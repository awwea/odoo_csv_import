#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sshtunnel
import psycopg2

try:
    with sshtunnel.SSHTunnelForwarder(('***', ***), ssh_username='root', ssh_password='***, remote_bind_address=('localhost', 5432), local_bind_address=('localhost', 5432)) as server:
        server.start()

        conn = psycopg2.connect(database='awwea', host='127.0.0.1', port=server.local_bind_port, user='postgres', password='VmGgssDA5TKKsAosG4tiXB')
        cr = conn.cursor()

        cr.execute("""SELECT LAST_VALUE FROM product_public_category_id_seq; """)
        rows = cr.fetchall()
        for row in rows:
            PRODUCT_PUB_CAT_SEQ = row[0]
            print(PRODUCT_PUB_CAT_SEQ)

        cr.execute("""SELECT LAST_VALUE FROM product_template_id_seq; """)
        rows = cr.fetchall()
        for row in rows:
            PRODUCT_TEMPLATE_SEQ = row[0]
            print(PRODUCT_TEMPLATE_SEQ)

        cr.execute("""SELECT LAST_VALUE FROM product_product_id_seq; """)
        rows = cr.fetchall()
        for row in rows:
            PRODUCT_PRODUCT_SEQ = row[0]
            print(PRODUCT_PRODUCT_SEQ)

        cr.execute("""SELECT number_next FROM ir_sequence WHERE code = 'product.product' and name LIKE '%Dropship%'; """)
        rows = cr.fetchall()
        for row in rows:
            PRODUCT_PRODUCT_REF_SEQ = row[0]
            print(PRODUCT_PRODUCT_REF_SEQ)

        cr.execute("""SELECT prefix FROM ir_sequence WHERE code = 'product.product' and name LIKE '%Sequence for Dropship Product%'; """)
        rows = cr.fetchall()
        for row in rows:
            PRODUCT_PRODUCT_PREFIX_SEQ = row[0]
            print(PRODUCT_PRODUCT_PREFIX_SEQ)

        cr.execute("""SELECT number_next FROM ir_sequence WHERE code = 'res.partner'; """)
        rows = cr.fetchall()
        for row in rows:
            PARTNER_REF_SEQ = row[0]
            print(PARTNER_REF_SEQ)

        cr.execute("""SELECT LAST_VALUE FROM product_image_id_seq; """)
        rows = cr.fetchall()
        for row in rows:
            PRODUCT_IMAGE_SEQ = row[0]
            print(PRODUCT_IMAGE_SEQ)

        cr.execute("""SELECT LAST_VALUE FROM ir_attachment_id_seq; """)
        rows = cr.fetchall()
        for row in rows:
            IR_ATTACHMENT_SEQ = row[0]
            print(IR_ATTACHMENT_SEQ)

        cr.execute("""SELECT LAST_VALUE FROM product_supplierinfo_id_seq; """)
        rows = cr.fetchall()
        for row in rows:
            PRODUCT_ID_SUPPLIER_SEQ = row[0]
            print(PRODUCT_ID_SUPPLIER_SEQ)

        cr.execute("""SELECT LAST_VALUE FROM product_brand_id_seq; """)
        rows = cr.fetchall()
        for row in rows:
            PRODUCT_BRAND_ID_SEQ = row[0]
            print(PRODUCT_BRAND_ID_SEQ)

        cr.execute("""SELECT LAST_VALUE FROM res_partner_id_seq; """)
        rows = cr.fetchall()
        for row in rows:
            PARTNER_ID_SEQ = row[0]
            print(PARTNER_ID_SEQ)

        conn.close()
        server.stop()
        print('\n Closing db connection... Stopping ssh server.... \n')
except:
    print('\n Connection failed...\n')
