#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import contextlib
import petl as etl
import numpy as np
from numpy import logical_and as _and, logical_or as _or
import pandas as pd
import math, csv, shutil

from tools.common import *
from tools.db_server import PRODUCT_TEMPLATE_SEQ, PRODUCT_PRODUCT_SEQ, PRODUCT_PRODUCT_REF_SEQ, PRODUCT_IMAGE_SEQ, IR_ATTACHMENT_SEQ, PRODUCT_ID_SUPPLIER_SEQ, PARTNER_ID_SEQ, PARTNER_REF_SEQ, PRODUCT_PRODUCT_PREFIX_SEQ, PRODUCT_BRAND_ID_SEQ, PRODUCT_PUB_CAT_SEQ


### Make Copy of Database to work on ###
shutil.copy2(SRC, DST) 
print('\n Making copy of database to work on it...\n')

with contextlib.closing(SQL3) as con:
    # S0 Load the data into a temp db
    try:
        # Filter some values and reduce attribute values qty
        cr = con.cursor()
        cr.executescript(SQL_TRANSFORM)
        con.commit()
        print('\n Working on temp db.... Changed some columns in db...\n')
    except:
        print(ERROR, 'S0')

    # S1 prepare data
    try:
        print('\n Starting preparing data...\n')
        df = pd.read_sql_query("""SELECT * FROM product """, con) #  WHERE regular_price is NOT '' or price IS NOT ''
        df['tmpl_img_name'] = df['image URL'].apply(lambda x: x.split('/')[-1])
        df['price'] = df['price'].apply(lambda x: x.split('-')[0])
        df[['price', 'regular_price']] = df[['price', 'regular_price']].apply(pd.to_numeric, errors='coerce')
        df['cost'] = df['price'].combine_first(df['regular_price'])
        ######### Calculate Public Price based on formula and add to DataFrame. Round Up to whole number 6.54 ==> 7 and then - 0.05 to become like 6.95 #########
        cost = df['cost']
        df['public_price'] = np.where(_or(cost <= 0, cost is None), 3.90,
                                                    np.where(_and(cost > 0, cost < 1), 4.98,
                                                np.where(_and(cost >= 1, cost < 1.5), 6.98,
                                            np.where(_and(cost >= 1.5, cost < 2), 7.98,
                                        np.where(_and(cost >= 2, cost < 3), 9.90,
                                    np.where(_and(cost >= 3, cost < 4), 11.90,
                                np.where(_and(cost >= 5, cost < 10), np.ceil(cost * 2.65) - 0.05,
                            np.where(_and(cost >= 10, cost < 25), np.ceil(cost * 2.4) - 0.05,
                        np.where(_and(cost >= 25, cost < 30), np.ceil(cost * 2) - 0.05,
                    np.where(_and(cost >= 30, cost < 50), np.ceil(cost * 1.85) - 0.05,
                np.where(_and(cost >= 50, cost < 100), np.ceil(cost * 1.65) - 0.05,
            np.where(_and(cost >= 100, cost < 200), np.ceil(cost * 1.55) - 0.05,
        np.where(cost >= 200, np.ceil(cost * 1.4) - 0.05, None)))))))))))))

        #### Product Template prepare table ####
        trans_0 = etl.addrownumbers(etl.fromdataframe(df), start=PRODUCT_TEMPLATE_SEQ + 1, field='PRODUCT_TEMPLATE_ID')
        trans_1 = etl.addrownumbers(trans_0, start=PRODUCT_ID_SUPPLIER_SEQ + 1, field='PRODUCT_ID_SUPPLIER')
        trans_2 = etl.addrownumbers(trans_1, start=PARTNER_ID_SEQ + 1, field='PARTNER_ID')
        trans_3 = etl.addrownumbers(trans_2, start=PRODUCT_IMAGE_SEQ + 1, field='PDODUCT_IMAGE_ID')
        trans_4 = etl.addrownumbers(trans_3, start=PRODUCT_PRODUCT_REF_SEQ, field='PRODUCT_INTERNAL_REF')
        trans_5 = etl.addrownumbers(trans_4, start=PARTNER_REF_SEQ + 1, field='PARTNER_REF')
        trans_6 = etl.addrownumbers(trans_5, start=IR_ATTACHMENT_SEQ + 1, field='IMAGE_ATTACHMENT_ID')
        trans_7 = etl.addrownumbers(trans_6, start=PRODUCT_BRAND_ID_SEQ + 1, field='PRODUCT_BRAND_ID')
        trans_8 = etl.addrownumbers(trans_7, start=PRODUCT_PUB_CAT_SEQ + 1, field='PPRODUCT_PUB_CAT_ID')
        trans_9 = etl.addfield(trans_8, 'PRODUCT_PREFIX_SEQ', PRODUCT_PRODUCT_PREFIX_SEQ)
        trans_10 = etl.convert(trans_9, ('product_name','product_category','vendor_name','vendor_country','brand_name','model','item_type','gender','item_material','item_style','item_pattern','item_fabric_type','item_waist_type','item_length','item_fit','item_thickness','item_age_group','item_season','item_version','item_elasticity','item_index','category','category 2'), 'title')
        PRODUCT_TEMPLATE_OUT = etl.addfield(trans_10, 'feedback_iframe', lambda row: '%s%s%s%s%s%s%s' % ("""<iframe scrolling="no" frameborder="0" marginwidth="0" marginheight="0" width="100%" height="2491" src="https://feedback.aliexpress.com/display/productEvaluation.htm?productId=""", row.vendor_product_code, """&amp;ownerMemberId=""", row.vendor_ext_id, """&amp;companyId=""", row.company_ext_id, """&amp;memberType=seller&amp;startValidDate=&amp;i18n=true" />"""))
        # etl.tocsv(PRODUCT_TEMPLATE_OUT, TRANSIT_TEMPLATE, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=csv.QUOTE_ALL)
        print('\n Product Template. Building Template. Added rows to file... %s \n' % TRANSIT_TEMPLATE)
    except Exception:
        print(ERROR, 'S1')


    #### 2. Product Attribute Color + Variant Images + Size ####
    ## Join images, color and size as product variants #
    try:
        df = pd.read_sql_query("""SELECT * FROM variant_1_color WHERE var_1_title IN ('White','Black','Grey','Gray','Navy','Rose','Red','Blue','Green','Purple','Silver','Gold','Coffee','Yellow','Pink','Multiple','Lavender','Camouflage','Brown','Skin','Orange','Khaki','Beige','Ivory','Burgundy','Wine','Mint','Candy','Neon','Fancy','Flowers','Geometric','Fuchsia','Cartoon','Nude','Stone','Chrome','Sapphire','Burgundy','Velvet','Turquoise','Print','Stripes','Shape','Patchwork','Diamond','Fluorescence','Love','Flag','Mermaid','Wave','Rainbow','Leopard','Tiger','Snake','Picture')""", con)

        df['var_img_name'] = df['var_1_img'].apply(lambda x: os.path.split(os.path.split(x)[0])[1]) + '_' + df['var_1_img'].apply(lambda x: x.split('/')[-1])

        PRODUCT_VAR_SIZE = etl.fromdb(con, """SELECT * FROM variant_2_size WHERE var_2_title not LIKE '%Siz%' """)
        PRODUCT_VARIANT_OUT = etl.outerjoin(etl.fromdataframe(df), PRODUCT_TEMPLATE_OUT, key=JOIN_KEY)
        # etl.fromcsv(TRANSIT_TEMPLATE, delimiter=DELIMITER, quotechar=QUOTECHAR)
        PRODUCT_VAR_SIZE_OUT = etl.outerjoin(PRODUCT_VAR_SIZE, PRODUCT_VARIANT_OUT, key=JOIN_KEY)
        trans = etl.addrownumbers(PRODUCT_VAR_SIZE_OUT, start=PRODUCT_PRODUCT_SEQ + 1, field='PRODUCT_PRODUCT_ID')
        PRODUCT_VARIANT = etl.rename(trans, {'category 2':'category_2', 'model':'Model', 'item_type':'Type', 'gender':'Gender', 'item_material':'Material', 'item_style':'Style', 'item_pattern':'Pattern', 'item_thickness':'Thickness', 'item_fabric_type':'Fabric', 'item_waist_type':'Waist', 'item_age_group':'Age', 'item_season':'Season', 'var_1_title':'Color', 'var_2_title':'Size'})
        etl.tocsv(PRODUCT_VARIANT, TRANSIT_VARIANT, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=csv.QUOTE_ALL)
        print('\n Combining product attributes Color/Images + Size. Joined tables to file... %s \n' % TRANSIT_VARIANT)
    except Exception:
        print(ERROR, 'S2')


    #### 3. Product Variant Images ####
    try:
        VARIANT_IMAGE = etl.cut(PRODUCT_VARIANT, 'id', 'product_name', 'PRODUCT_PRODUCT_ID', 'var_img_name')
        etl.tocsv(VARIANT_IMAGE, TRANSIT_VAR_IMAGE, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=csv.QUOTE_ALL)
        print('\n Product Variant Images. Creating file... %s \n' % TRANSIT_VAR_IMAGE)
    except Exception:
        print(ERROR, 'S3')


    #### 4. Product Template Multi Images for Ir.Attachment ####
    ## Join images & product templates #
    try:
        INPUT_PRODUCT_IMAGE = etl.fromdb(con, """SELECT * FROM media""")
        PRODUCT_TEMPLATE = etl.cut(PRODUCT_TEMPLATE_OUT, 'id', 'product_name', 'PDODUCT_IMAGE_ID', 'IMAGE_ATTACHMENT_ID', 'PRODUCT_TEMPLATE_ID')
        PRODUCT_IMAGE_OUT = etl.join(INPUT_PRODUCT_IMAGE, PRODUCT_TEMPLATE, key=JOIN_KEY)
        etl.tocsv(PRODUCT_IMAGE_OUT, TRANSIT_IMAGE, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=csv.QUOTE_ALL)
        print('\n Product Template Multi Images to file... %s \n' % TRANSIT_IMAGE)
    except Exception:
        print(ERROR, 'S4')

    
    #### 5. Product Template in Websites ####
    try:
        trans_0 = etl.cut(PRODUCT_TEMPLATE_OUT, 'PRODUCT_TEMPLATE_ID', 'id')
        trans_1 = etl.addfield(trans_0, 'website_id', 2)
        # trans_2 = etl.rename(trans_1, 'PRODUCT_TEMPLATE_ID', 'product_template_id')
        write_to_csv = trans_1
        etl.tocsv(write_to_csv, TRANSIT_PRODUCT_WEBSITE, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=csv.QUOTE_ALL)
        print('\n Bindings made to %s \n' % TRANSIT_PRODUCT_WEBSITE)
    except Exception:
        print(ERROR, 'S5')


    #### 6. Download Variant Images ####
    try:
        #subprocess.call('python3 tools/download.py 1', shell=True)
        print('\n Download Variant Images. Download finished... \n')
    except Exception:
        print(ERROR, 'S6')


if os.path.exists(DST):
    #os.unlink(DST)
    print('\n Removing db file: %s... \n' % DB_File)
else:
    print('File: %s does not exists' % DST)


print('\n All done...\n')
subprocess.call(['pyclean .; py3clean .'], shell = True)
