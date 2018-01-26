#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

from csv_tools.lib.transform import ProductProcessorV10 as Proc
from csv_tools.lib import mapper

from tools.common import *
from tools.prefix import *
from tools.colors import *
from tools.maps import *


######### Load File #########
processor = Proc(TRANSIT_VARIANT, delimiter=DELIMITER)

######### CONTEXT TEMPLATE NO create_product_variant #########
context = {'create_product_product': False, 'tracking_disable': True}


# STEP : Category and Parent Category
######################################################################
categ_parent_map = {
    'id': mapper.m2o(CATEGORY_PREFIX, 'category'),
    'name': mapper.val('category'),
    'product_type_id': mapper.const('Dropshipping'),
    'no_create_variant': mapper.const('0'),
}
#processor.process(categ_parent_map, 'DATA1/product.category.parent.csv', {'worker': 2, 'batch_size': 10, 'model': 'product.category'}, 'set')
categ_map = {
    'id': mapper.m2o(CATEGORY_PREFIX, 'Sub Category'),
    'parent_id/id': mapper.m2o(CATEGORY_PREFIX, 'category'),
    'name': mapper.val('Sub Category'),
    'product_type_id': mapper.const('Dropshipping'),
    'no_create_variant': mapper.const('0'),
}
#processor.process(categ_map, 'DATA1/product.category.csv', {'worker': 2, 'batch_size': 20}, 'set')


# STEP : Public Categories
######################################################################
pub_categ_map = {
    'id': mapper.m2o(PUB_CATEGORY_PREFIX, 'PPRODUCT_PUB_CAT_ID'),
    'name': mapper.val('category'),
    'sequence': mapper.const('10'),
    'website_meta_title': mapper.const(''),
    'website_meta_keaywords': mapper.const(''),
    'website_meta_description': mapper.const(''),
}
processor.process(pub_categ_map, 'DATA1/product.public.category.parent.csv', {'worker': 2, 'batch_size': 10, 'model': 'product.category'}, 'set')

pub_sub_categ_map = {
    'id': mapper.m2m_id_list(PUB_CATEGORY_PREFIX, 'category_2'),
    'parent_id/id': mapper.m2o(PUB_CATEGORY_PREFIX, 'PPRODUCT_PUB_CAT_ID'),
    'name': mapper.val('category_2'),
    'sequence': mapper.const('10'),
    'website_meta_title': mapper.const(''),
    'website_meta_keaywords': mapper.const(''),
    'website_meta_description': mapper.const(''),
}
processor.process(pub_sub_categ_map, 'DATA1/product.public.category.csv', {'worker': 2, 'batch_size': 20}, m2m=True)



# STEP : Product Template (with variants, set context:False for no variants)
######################################################################
template_map = {
    'id': mapper.m2o(TEMPLATE_PREFIX, 'PRODUCT_TEMPLATE_ID'),
    #'categ_id/id': mapper.m2o(CATEGORY_PREFIX, 'Sub Category'),
    'categ_id/id': mapper.const('product_type_template.product_category_dropship'),
    'product_type_id': mapper.const('Dropshipping'),
    'name': mapper.val('product_name'),
    'website_published': mapper.const('0'),
    'standard_price': mapper.num('cost'),
    'map_price': mapper.num('cost'),
    'list_price': mapper.num('public_price'),
    'default_code': mapper.concat_mapper_all('', mapper.val('PRODUCT_PREFIX_SEQ'), mapper.val('PRODUCT_INTERNAL_REF')),
    'weight': mapper.val('weight'),
    'uom_id': mapper.const('Unit(s)'),
    'length': mapper.val('length'),
    'width': mapper.val('width'),
    'height': mapper.val('height'),
    'produce_delay': mapper.val('max_delay'),
    'sale_delay': mapper.val('max_delay'),
    'dimensional_uom_id': mapper.const('cm'),
    'mfg_id': mapper.const('Aliexpress'),
    'mfg_product_code': mapper.val('vendor_product_code'),
    'mfg_product_url': mapper.concat_mapper_all('', mapper.const('https://aliexpress.com/wholesale?&SearchText='), mapper.val('vendor_product_code')),
    'description_sale': mapper.val('specific_description'),
    'description_purchase': mapper.val('description_vendor'),
    #'image_medium': mapper.binary('tmpl_img_name', 'IMG_DIR', skip=True),
    'public_categ_ids': mapper.m2m(PUB_CATEGORY_PREFIX, 'category_2'),
}
processor.process(template_map, 'DATA1/product.template.csv', {'worker': 5, 'batch_size': 50, 'context': context}, 'set')



# STEP : NO Variants Attribute List as specified
######################################################################
ATTRIBUTE_LIST_NO_VAR = attribute_list_no_create_variant
processor.process_attribute_data(ATTRIBUTE_LIST_NO_VAR, ATTRIBUTE_PREFIX, 'DATA2/product.attribute.csv', {'worker': 1, 'batch_size': 10, 'context': context})

# STEP : NO Variants Attribute Value
######################################################################
attribute_value_map = {
    'id': mapper.m2m_id_list(ATTRIBUTE_VALUE_PREFIX, *[mapper.concat_field_value_m2m('_', f) for f in ATTRIBUTE_LIST_NO_VAR]),
    'name': mapper.m2m_value_list(*ATTRIBUTE_LIST_NO_VAR),
    'attribute_id/id': mapper.m2m_id_list(ATTRIBUTE_PREFIX, *[mapper.field(f) for f in ATTRIBUTE_LIST_NO_VAR]),
    #'html_color': mapper.val('Color'),
}
processor.process(attribute_value_map, 'DATA2/product.attribute.value.csv', {'worker': 2, 'batch_size': 50, 'context': context, 'groupby': 'attribute_id/id'}, m2m=True)

# STEP : NO Variants Attribute Value Line
######################################################################
attribute_line_map = {
    'id': mapper.m2m_id_list(ATTRIBUTE_LINE_PREFIX, *[mapper.concat_mapper_all('_', mapper.field(f), mapper.val('PRODUCT_TEMPLATE_ID')) for f in ATTRIBUTE_LIST_NO_VAR]),
    'product_tmpl_id/id': mapper.m2o(TEMPLATE_PREFIX, 'PRODUCT_TEMPLATE_ID'),
    'attribute_id/id': mapper.m2m_id_list(ATTRIBUTE_PREFIX, *[mapper.field(f) for f in ATTRIBUTE_LIST_NO_VAR]),
    'value_ids/id': mapper.m2m_id_list(ATTRIBUTE_VALUE_PREFIX, *[mapper.concat_field_value_m2m('_', f) for f in ATTRIBUTE_LIST_NO_VAR]),
}
context['update_many2many'] = True
processor.process(attribute_line_map, 'DATA2/product.attribute.line.csv', {'worker': 5, 'batch_size': 50, 'context': dict(context), 'groupby': 'product_tmpl_id/id'}, m2m=True)
context.pop('update_many2many')


######################################################################
######################################################################
######################################################################


######### CONTEXT create_product_variant #########
context = {'create_product_product': True, 'tracking_disable': True}

# STEP : Attribute List as specified WITH Variants
######################################################################
ATTRIBUTE_LIST = attribute_list_with_variant
processor.process_attribute_data(ATTRIBUTE_LIST, ATTRIBUTE_PREFIX, 'DATA1/product.attribute.csv', {'worker': 1, 'batch_size': 10, 'context': context})


# STEP : Attribute Value
######################################################################
attribute_value_map = {
    'id': mapper.m2m_id_list(ATTRIBUTE_VALUE_PREFIX, *[mapper.concat_field_value_m2m('_', f) for f in ATTRIBUTE_LIST]),
    'name': mapper.m2m_value_list(*ATTRIBUTE_LIST),
    'attribute_id/id': mapper.m2m_id_list(ATTRIBUTE_PREFIX, *[mapper.field(f) for f in ATTRIBUTE_LIST]),
    'html_color': mapper.map_val('Color', color_map),
}
processor.process(attribute_value_map, 'DATA1/product.attribute.value.csv', {'worker': 2, 'batch_size': 50, 'context': context, 'groupby': 'attribute_id/id'}, m2m=True)


# STEP : Attribute Value Line
######################################################################
attribute_line_map = {
    'id': mapper.m2m_id_list(ATTRIBUTE_LINE_PREFIX, *[mapper.concat_mapper_all('_', mapper.field(f), mapper.val('PRODUCT_TEMPLATE_ID')) for f in ATTRIBUTE_LIST]),
    'product_tmpl_id/id': mapper.m2o(TEMPLATE_PREFIX, 'PRODUCT_TEMPLATE_ID'),
    'attribute_id/id': mapper.m2m_id_list(ATTRIBUTE_PREFIX, *[mapper.field(f) for f in ATTRIBUTE_LIST]),
    'value_ids/id': mapper.m2m_id_list(ATTRIBUTE_VALUE_PREFIX, *[mapper.concat_field_value_m2m('_', f) for f in ATTRIBUTE_LIST]),
}
context['update_many2many'] = True
processor.process(attribute_line_map, 'DATA1/product.attribute.line.csv', {'worker': 5, 'batch_size': 50, 'context': dict(context), 'groupby': 'product_tmpl_id/id'}, m2m=True)
context.pop('update_many2many')


# STEP : Product Variant
######################################################################
product_variant_map = {
    'id': mapper.m2o_map(PRODUCT_PREFIX, mapper.concat('_', 'PRODUCT_PRODUCT_ID', 'Color', 'Size'), skip=False),
    #'barcode': mapper.val('barcode'),
    #'default_code': mapper.val('PRODUCT_INTERNAL_REF')
    #'name': mapper.concat_mapper_all('-', mapper.val('ITEM_SKU'), mapper.val('Color'), mapper.val('Gender'), mapper.val('Size_H'), mapper.val('Size_W')),
    'standard_price': mapper.num('cost'),
    'lst_price': mapper.num('public_price'),
    #'dimensional_uom_id': mapper.val('uom'),
    'product_tmpl_id/id': mapper.m2o(TEMPLATE_PREFIX, 'PRODUCT_TEMPLATE_ID'),
    'attribute_value_ids/id': mapper.m2m_attribute_value(ATTRIBUTE_VALUE_PREFIX, 'Color', 'Size'),
    #'image_medium': mapper.binary('variant_img', 'VAR_IMG_DIR', skip=True),
}
processor.process(product_variant_map, 'DATA1/product.product.csv', {'worker': 5, 'batch_size': 50, 'groupby': 'product_tmpl_id/id', 'context': context}, 'set')


# STEP : Product Supplier
######################################################################
product_supplier_map = {
    'id': mapper.m2o(PRODUCT_SUPPLIER_PREFIX, 'PRODUCT_ID_SUPPLIER'),
    'name': mapper.m2o(PARTNER_SUPPLIER_PREFIX, 'PARTNER_ID'),
    'product_tmpl_id/id': mapper.m2o(TEMPLATE_PREFIX, 'PRODUCT_TEMPLATE_ID'),
    'product_code': mapper.val('vendor_product_code'),
    'product_name': mapper.val('product_name'),
    'min_qty': mapper.const('1'),
    'price': mapper.num('cost'),
    #'price': mapper.num('regular_price'),
    'delay': mapper.val('max_delay'),
    'currency_id': mapper.val('currency'),
}
processor.process(product_supplier_map, 'DATA1/product.supplierinfo.csv', { 'worker' : 2, 'batch_size' : 50, 'groupby' : 'product_tmpl_id/id', 'context' : context}, 'set')
partner_supplier_map = {
    'id': mapper.m2o(PARTNER_SUPPLIER_PREFIX, 'PARTNER_ID'),
    'name': mapper.val('vendor_name'),
    'ref': mapper.val('PARTNER_REF'),
    #'lang': mapper.map_val('vendor_lang', lang_map),
    #'vat': mapper.val(''),
    'website': mapper.val('vendor_website'),
    'country_id/id': mapper.map_val('vendor_country', country_map),
    'is_company': mapper.const('1'),
    'customer': mapper.const('0'),
    'supplier': mapper.const('1'),
    'picking_warn': mapper.const('no-message'),
    'sale_warn': mapper.const('no-message'),
    'purchase_warn': mapper.const('no-message'),
    'invoice_warn': mapper.const('no-message'),
}
processor.process(partner_supplier_map, 'DATA1/res_partner.csv', {'worker': 2, 'batch_size': 50}, 'set')


# STEP : Product Brand
######################################################################
product_brand_map = {
    'id': mapper.m2o(PRODUCT_BRAND_PREFIX, 'PRODUCT_BRAND_ID'),
    'name': mapper.val('brand_name'),
    'product_tmpl_id/id': mapper.m2o(TEMPLATE_PREFIX, 'PRODUCT_TEMPLATE_ID'),
    'partner_id/id': mapper.m2o(PARTNER_SUPPLIER_PREFIX, 'PARTNER_ID'),
    #'description': mapper.val('feedback_iframe'),
}
processor.process(product_brand_map, 'DATA1/product.brand.csv', { 'worker' : 2, 'batch_size' : 50, 'groupby' : 'product_tmpl_id/id', 'context' : context}, 'set')



# STEP : Product Images
######################################################################
######################################################################

#  Product Template Multi Images
######################################################################
img_processor = Proc(TRANSIT_IMAGE, delimiter=DELIMITER)

image_url_map = {
    'id': mapper.m2o(IMAGE_URL_PREFIX, 'PDODUCT_IMAGE_ID'),
    'name': mapper.val('product_name'),
    'product_tmpl_id/id': mapper.m2o(TEMPLATE_PREFIX, 'PRODUCT_TEMPLATE_ID'),
}
img_processor.process(image_url_map, 'DATA1/product.image.csv', {'worker': 4, 'batch_size': 50, 'groupby' : 'product_tmpl_id/id', 'context' : context},  'set')

image_url_attachment_map = {
    'id': mapper.m2o(IMAGE_URL_PREFIX, 'IMAGE_ATTACHMENT_ID'),
    'name': mapper.const('image'),
    'index_content': mapper.const(''),
    'res_field': mapper.const('image'),
    'type': mapper.const('url'),
    'res_name': mapper.val('product_name'),
    'url': mapper.val('media_images'),
    'binary': mapper.const(''),
    'res_model': mapper.const('product.image'),
    'res_id': mapper.val('PDODUCT_IMAGE_ID'),
}
img_processor.process(image_url_attachment_map, 'DATA1/ir.attachment.csv', {'worker': 2, 'batch_size': 10}, 'set')


#  Product Variant Images
######################################################################
img_var_processor = Proc(TRANSIT_VAR_IMAGE, delimiter=DELIMITER)

image_var_map = {
    'id': mapper.m2o(PRODUCT_PREFIX, 'PRODUCT_PRODUCT_ID'),
    #'image_medium': mapper.binary('var_img_name', VAR_IMG_DIR, skip=True),
}
img_var_processor.process(image_var_map, 'DATA2/product.product.csv', {'worker': 2, 'batch_size': 10}, 'set')


###############################################
## FINAL: Define output and import parameter ##
###############################################

processor.write_to_file('_product_import.sh', python_exe='python-coverage run -a', path='../')
img_processor.write_to_file('_product_image_import.sh', python_exe='python-coverage run -a', path='../')
img_var_processor.write_to_file('_product_var_image_import.sh', python_exe='python-coverage run -a', path='../')


print('\n All done...\n')
subprocess.call(['pyclean . && py3clean . && rm -rf .coverage'], shell = True)
