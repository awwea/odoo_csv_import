# -*- coding: utf-8 -*-

import os
import sqlite3


DELIMITER = '|'
QUOTECHAR = '"'
JOIN_KEY = 'id'

ERROR = """\n Something has gone wrong... Try it better! ;-)\n"""

attribute_list_with_variant = ['Color','Size']
attribute_list_no_create_variant = ['Thickness','Gender','Style','Pattern','Age',]

IMG_DIR = 'TEMPLATE_IMAGES'
VAR_IMG_DIR = 'VARIANT_IMAGES'
TRANSIT = 'transit'
#TRANSIT = '/dev/shm/transit'
dirs = [TRANSIT,IMG_DIR,VAR_IMG_DIR,'DATA','DATA1','DATA2']
for dir in dirs:
    if not os.path.exists(dir):
        os.makedirs(dir)

TRANSIT_TEMPLATE = os.path.join(TRANSIT, 'product_template.csv')
TRANSIT_IMAGE = os.path.join(TRANSIT, 'product_template_images.csv')
TRANSIT_VARIANT = os.path.join(TRANSIT, 'product_variant.csv')
TRANSIT_VAR_IMAGE = os.path.join(TRANSIT, 'product_variant_images.csv')
TRANSIT_PRODUCT_WEBSITE = os.path.join(TRANSIT, 'product_template_website_rel.csv')

DB_File = 'leggings.db'
SRC = os.path.join('SRC', DB_File)
DST = os.path.join(TRANSIT, DB_File)
SQL3 = sqlite3.connect(DST)

SQL_TRANSFORM = """
DELETE FROM product WHERE product_name = '';

UPDATE product SET gender = 'Female' WHERE gender LIKE '%Wom%';
UPDATE product SET gender = 'Female' WHERE gender LIKE '%Fem%';
UPDATE product SET gender = 'Male' WHERE gender LIKE '%Man%';
UPDATE product SET gender = 'Male' WHERE gender LIKE '%Men%';
UPDATE product SET gender = 'Male' WHERE gender LIKE '%Male%';
UPDATE product SET gender = 'Uni' WHERE gender NOT IN ('Female','Male');

UPDATE product SET item_age_group = 'Adult' WHERE item_age_group LIKE '%Adu%';
UPDATE product SET item_age_group = 'Adult' WHERE item_age_group LIKE '%Wom%';
UPDATE product SET item_age_group = 'Adult' WHERE item_age_group LIKE '%Man%';
UPDATE product SET item_age_group = 'Teenager' WHERE item_age_group LIKE '%Teen%';
UPDATE product SET item_age_group = 'Teenager' WHERE item_age_group LIKE '%Boy%';
UPDATE product SET item_age_group = 'Teenager' WHERE item_age_group LIKE '%Girl%';
UPDATE product SET item_age_group = 'Uni' WHERE item_age_group NOT IN ('Adult','Teenager');

UPDATE variant_2_size SET var_2_title = 'Uni' WHERE var_2_title LIKE '%One%';
UPDATE variant_2_size SET var_2_title = 'S' WHERE var_2_title LIKE '%42%';
UPDATE variant_2_size SET var_2_title = 'M' WHERE var_2_title LIKE '%46%';
UPDATE variant_2_size SET var_2_title = 'L' WHERE var_2_title LIKE '%50%';
UPDATE variant_2_size SET var_2_title = 'XL' WHERE var_2_title LIKE '%54%';
UPDATE variant_2_size SET var_2_title = 'XXL' WHERE var_2_title LIKE '%58%';
UPDATE variant_2_size SET var_2_title = 'S' WHERE var_2_title NOT IN ('4XS','XXXS','XXS','XS','S','M','L','XL','XXL','XXXL','4XL','5XL','6XL','7XL','8XL','Sizing info','Uni','One size');

UPDATE variant_1_color SET var_1_title = 'White' WHERE var_1_title LIKE '%Whit%';
UPDATE variant_1_color SET var_1_title = 'White' WHERE var_1_title LIKE '%Wt%';
UPDATE variant_1_color SET var_1_title = 'White' WHERE var_1_title LIKE '%Wh%';
UPDATE variant_1_color SET var_1_title = 'White' WHERE var_1_title LIKE '%We%';
UPDATE variant_1_color SET var_1_title = 'White' WHERE var_1_title = '01';
UPDATE variant_1_color SET var_1_title = 'White' WHERE var_1_title = 'color1';
UPDATE variant_1_color SET var_1_title = 'White' WHERE var_1_title LIKE '% 1%';
UPDATE variant_1_color SET var_1_title = 'White' WHERE var_1_title = '1';
UPDATE variant_1_color SET var_1_title = 'Black' WHERE var_1_title LIKE '%Black%';
UPDATE variant_1_color SET var_1_title = 'Black' WHERE var_1_title LIKE '%Bk%';
UPDATE variant_1_color SET var_1_title = 'Black' WHERE var_1_title LIKE '%Bla%';
UPDATE variant_1_color SET var_1_title = 'Black' WHERE var_1_title LIKE '%Bal%';
UPDATE variant_1_color SET var_1_title = 'Black' WHERE var_1_title = 'color2';
UPDATE variant_1_color SET var_1_title = 'Black' WHERE var_1_title = '02';
UPDATE variant_1_color SET var_1_title = 'Black' WHERE var_1_title LIKE '% 2%';
UPDATE variant_1_color SET var_1_title = 'Black' WHERE var_1_title = '2';
UPDATE variant_1_color SET var_1_title = 'Gray' WHERE var_1_title LIKE '%Grey%';
UPDATE variant_1_color SET var_1_title = 'Gray' WHERE var_1_title LIKE '%Gray%';
UPDATE variant_1_color SET var_1_title = 'Gray' WHERE var_1_title LIKE '%Gy%';
UPDATE variant_1_color SET var_1_title = 'Gray' WHERE var_1_title = 'color3';
UPDATE variant_1_color SET var_1_title = 'Gray' WHERE var_1_title = '03';
UPDATE variant_1_color SET var_1_title = 'Gray' WHERE var_1_title LIKE '% 3%';
UPDATE variant_1_color SET var_1_title = 'Gray' WHERE var_1_title = '3';
UPDATE variant_1_color SET var_1_title = 'Navy' WHERE var_1_title LIKE '%Nav%';
UPDATE variant_1_color SET var_1_title = 'Rose' WHERE var_1_title LIKE '%Ros%';
UPDATE variant_1_color SET var_1_title = 'Wine' WHERE var_1_title LIKE '%Win%';
UPDATE variant_1_color SET var_1_title = 'Green' WHERE var_1_title LIKE '%Green%';
UPDATE variant_1_color SET var_1_title = 'Green' WHERE var_1_title LIKE '%arm%';
UPDATE variant_1_color SET var_1_title = 'Green' WHERE var_1_title LIKE '%gree%';
UPDATE variant_1_color SET var_1_title = 'Green' WHERE var_1_title LIKE '%12%';
UPDATE variant_1_color SET var_1_title = 'Purple' WHERE var_1_title LIKE '%purp%';
UPDATE variant_1_color SET var_1_title = 'Purple' WHERE var_1_title LIKE '%pur%';
UPDATE variant_1_color SET var_1_title = 'Silver' WHERE var_1_title LIKE '%silv%';
UPDATE variant_1_color SET var_1_title = 'Gold' WHERE var_1_title LIKE '%gold%';
UPDATE variant_1_color SET var_1_title = 'Gold' WHERE var_1_title LIKE '%gol%';
UPDATE variant_1_color SET var_1_title = 'Gold' WHERE var_1_title LIKE '%gd%';
UPDATE variant_1_color SET var_1_title = 'Coffee' WHERE var_1_title LIKE '%cof%';
UPDATE variant_1_color SET var_1_title = 'Yellow' WHERE var_1_title LIKE '%yello%';
UPDATE variant_1_color SET var_1_title = 'Pink' WHERE var_1_title LIKE '%Pink%';
UPDATE variant_1_color SET var_1_title = 'Pink' WHERE var_1_title LIKE '%pk%';
UPDATE variant_1_color SET var_1_title = 'Pink' WHERE var_1_title LIKE '%pin%';
UPDATE variant_1_color SET var_1_title = 'Multiple' WHERE var_1_title LIKE '%Mult%';
UPDATE variant_1_color SET var_1_title = 'Multiple' WHERE var_1_title LIKE '%Mc%';
UPDATE variant_1_color SET var_1_title = 'Multiple' WHERE var_1_title LIKE '%mix%';
UPDATE variant_1_color SET var_1_title = 'Multiple' WHERE var_1_title LIKE '%mul%';
UPDATE variant_1_color SET var_1_title = 'Multiple' WHERE var_1_title = 'color4';
UPDATE variant_1_color SET var_1_title = 'Multiple' WHERE var_1_title = '04';
UPDATE variant_1_color SET var_1_title = 'Multiple' WHERE var_1_title LIKE '% 4%';
UPDATE variant_1_color SET var_1_title = 'Multiple' WHERE var_1_title = '4';
UPDATE variant_1_color SET var_1_title = 'Multiple' WHERE var_1_title = 'compl';
UPDATE variant_1_color SET var_1_title = 'Blue' WHERE var_1_title LIKE '%bl%';
UPDATE variant_1_color SET var_1_title = 'Blue' WHERE var_1_title LIKE '%lb%';
UPDATE variant_1_color SET var_1_title = 'Blue' WHERE var_1_title = 'color5';
UPDATE variant_1_color SET var_1_title = 'Blue' WHERE var_1_title = '05';
UPDATE variant_1_color SET var_1_title = 'Blue' WHERE var_1_title LIKE '% 5%';
UPDATE variant_1_color SET var_1_title = 'Blue' WHERE var_1_title = '5';
UPDATE variant_1_color SET var_1_title = 'Lavender' WHERE var_1_title LIKE '%Laven%';
UPDATE variant_1_color SET var_1_title = 'Leopard' WHERE var_1_title LIKE '%leopard%';
UPDATE variant_1_color SET var_1_title = 'Snake' WHERE var_1_title LIKE '%snake%';
UPDATE variant_1_color SET var_1_title = 'Camouflage' WHERE var_1_title LIKE '%Camou%';
UPDATE variant_1_color SET var_1_title = 'Camouflage' WHERE var_1_title LIKE '%Camu%';
UPDATE variant_1_color SET var_1_title = 'Camouflage' WHERE var_1_title = 'color6';
UPDATE variant_1_color SET var_1_title = 'Camouflage' WHERE var_1_title = '06';
UPDATE variant_1_color SET var_1_title = 'Camouflage' WHERE var_1_title LIKE '% 6%';
UPDATE variant_1_color SET var_1_title = 'Camouflage' WHERE var_1_title = '6';
UPDATE variant_1_color SET var_1_title = 'Brown' WHERE var_1_title LIKE '%Brow%';
UPDATE variant_1_color SET var_1_title = 'Brown' WHERE var_1_title = 'color7';
UPDATE variant_1_color SET var_1_title = 'Brown' WHERE var_1_title = '07';
UPDATE variant_1_color SET var_1_title = 'Brown' WHERE var_1_title LIKE '% 7%';
UPDATE variant_1_color SET var_1_title = 'Brown' WHERE var_1_title = '7';
UPDATE variant_1_color SET var_1_title = 'Skin' WHERE var_1_title LIKE '%skin%';
UPDATE variant_1_color SET var_1_title = 'Orange' WHERE var_1_title LIKE '%Orange%';
UPDATE variant_1_color SET var_1_title = 'Orange' WHERE var_1_title LIKE '% 10%';
UPDATE variant_1_color SET var_1_title = 'Orange' WHERE var_1_title = '10';
UPDATE variant_1_color SET var_1_title = 'Khaki' WHERE var_1_title LIKE '%khaki%';
UPDATE variant_1_color SET var_1_title = 'Khaki' WHERE var_1_title LIKE '%kak%';
UPDATE variant_1_color SET var_1_title = 'Khaki' WHERE var_1_title LIKE '% 11%';
UPDATE variant_1_color SET var_1_title = 'Khaki' WHERE var_1_title = '11';
UPDATE variant_1_color SET var_1_title = 'Beige' WHERE var_1_title LIKE '%Beig%';
UPDATE variant_1_color SET var_1_title = 'Beige' WHERE var_1_title LIKE '%Baig%';
UPDATE variant_1_color SET var_1_title = 'Beige' WHERE var_1_title = 'color9';
UPDATE variant_1_color SET var_1_title = 'Beige' WHERE var_1_title = '09';
UPDATE variant_1_color SET var_1_title = 'Beige' WHERE var_1_title LIKE '% 9%';
UPDATE variant_1_color SET var_1_title = 'Beige' WHERE var_1_title = '9';
UPDATE variant_1_color SET var_1_title = 'Ivory' WHERE var_1_title LIKE '%Ivor%';
UPDATE variant_1_color SET var_1_title = 'Burgundy' WHERE var_1_title LIKE '%Burgun%';
UPDATE variant_1_color SET var_1_title = 'Mint' WHERE var_1_title LIKE '%Mint%';
UPDATE variant_1_color SET var_1_title = 'Candy' WHERE var_1_title LIKE '%cand%';
UPDATE variant_1_color SET var_1_title = 'Neon' WHERE var_1_title LIKE '%Neo%';
UPDATE variant_1_color SET var_1_title = 'Fancy' WHERE var_1_title LIKE '%Fanc%';
UPDATE variant_1_color SET var_1_title = 'Flowers' WHERE var_1_title LIKE '%Flower%';
UPDATE variant_1_color SET var_1_title = 'Flowers' WHERE var_1_title LIKE '%flor%';
UPDATE variant_1_color SET var_1_title = 'Geometric' WHERE var_1_title LIKE '%Geom%';
UPDATE variant_1_color SET var_1_title = 'Fuchsia' WHERE var_1_title LIKE '%Fuchsia%';
UPDATE variant_1_color SET var_1_title = 'Cartoon' WHERE var_1_title LIKE '%Cart%';
UPDATE variant_1_color SET var_1_title = 'Nude' WHERE var_1_title LIKE '%nud%';
UPDATE variant_1_color SET var_1_title = 'Stone' WHERE var_1_title LIKE '%ston%';
UPDATE variant_1_color SET var_1_title = 'Chrome' WHERE var_1_title LIKE '%Chrom%';
UPDATE variant_1_color SET var_1_title = 'Sapphire' WHERE var_1_title LIKE '%Sapphir%';
UPDATE variant_1_color SET var_1_title = 'Velvet' WHERE var_1_title LIKE '%Velvet%';
UPDATE variant_1_color SET var_1_title = 'Turquoise' WHERE var_1_title LIKE '%turq%';
UPDATE variant_1_color SET var_1_title = 'Red' WHERE var_1_title = 'color8';
UPDATE variant_1_color SET var_1_title = 'Red' WHERE var_1_title = '08';
UPDATE variant_1_color SET var_1_title = 'Red' WHERE var_1_title LIKE '% 8%';
UPDATE variant_1_color SET var_1_title = 'Red' WHERE var_1_title = '8';
UPDATE variant_1_color SET var_1_title = 'Red' WHERE var_1_title LIKE '%Red%';
UPDATE variant_1_color SET var_1_title = 'Print' WHERE var_1_title LIKE '%Prin%';
UPDATE variant_1_color SET var_1_title = 'Stripes' WHERE var_1_title LIKE '%strip%';
UPDATE variant_1_color SET var_1_title = 'Shape' WHERE var_1_title LIKE '%shap%';
UPDATE variant_1_color SET var_1_title = 'Patchwork' WHERE var_1_title LIKE '%Patch%';
UPDATE variant_1_color SET var_1_title = 'Patchwork' WHERE var_1_title LIKE '%Path%';
UPDATE variant_1_color SET var_1_title = 'Diamond' WHERE var_1_title LIKE '%diamon%';
UPDATE variant_1_color SET var_1_title = 'Fluorescence' WHERE var_1_title LIKE '%Fluor%';
UPDATE variant_1_color SET var_1_title = 'Love' WHERE var_1_title LIKE '%love%';
UPDATE variant_1_color SET var_1_title = 'Flag' WHERE var_1_title LIKE '%flag%';
UPDATE variant_1_color SET var_1_title = 'Wave' WHERE var_1_title LIKE '%wave%';
UPDATE variant_1_color SET var_1_title = 'Rainbow' WHERE var_1_title LIKE '%Rain%';
UPDATE variant_1_color SET var_1_title = 'Mermaid' WHERE var_1_title LIKE '%Merm%';
UPDATE variant_1_color SET var_1_title = 'Leopard' WHERE var_1_title LIKE '%leo%';
UPDATE variant_1_color SET var_1_title = 'Tiger' WHERE var_1_title LIKE '%tiger%';
UPDATE variant_1_color SET var_1_title = 'Picture' WHERE var_1_title LIKE '%pic%';
UPDATE variant_1_color SET var_1_title = 'Picture' WHERE var_1_title LIKE '%see%';
UPDATE variant_1_color SET var_1_title = 'Picture' WHERE var_1_title LIKE '%as%';

UPDATE product SET item_waist_type = 'High' WHERE item_waist_type LIKE '%heigh%';
UPDATE product SET item_waist_type = 'High' WHERE item_waist_type LIKE '%high%';
UPDATE product SET item_waist_type = 'Low' WHERE item_waist_type LIKE '%low%';
UPDATE product SET item_waist_type = 'Mid' WHERE item_waist_type LIKE '%mid%';
UPDATE product SET item_waist_type = 'Mid' WHERE item_waist_type  NOT IN ('High','Mid','Low');

UPDATE product SET item_length = 'Ankle' WHERE item_length LIKE '%Ankle%';
UPDATE product SET item_length = 'Mid-Calf' WHERE item_length LIKE '%Mid-Calf%';
UPDATE product SET item_length = 'Knee' WHERE item_length LIKE '%Knee%';
UPDATE product SET item_length = 'Knee' WHERE item_length  NOT IN ('Ankle','Mid-Calf','Knee');

UPDATE product SET item_thickness = 'Thin' WHERE item_thickness LIKE '%thin%';
UPDATE product SET item_thickness = 'Thick' WHERE item_thickness LIKE '%thick%';
UPDATE product SET item_thickness = 'Normal' WHERE item_thickness LIKE '%Stand%';
UPDATE product SET item_thickness = 'Normal' WHERE item_thickness NOT IN ('Thin','Thick','Normal');

UPDATE product SET item_pattern = 'Solid' WHERE item_pattern LIKE '%solid%';
UPDATE product SET item_pattern = 'Patchwork' WHERE item_pattern LIKE '%path%';
UPDATE product SET item_pattern = 'Patchwork' WHERE item_pattern LIKE '%patch%';
UPDATE product SET item_pattern = 'Flowers' WHERE item_pattern LIKE '%flower%';
UPDATE product SET item_pattern = 'Flowers' WHERE item_pattern LIKE '%flor%';
UPDATE product SET item_pattern = 'Stripes' WHERE item_pattern LIKE '%strip%';
UPDATE product SET item_pattern = 'Skull' WHERE item_pattern LIKE '%skul%';
UPDATE product SET item_pattern = 'Animal' WHERE item_pattern LIKE '%anim%';
UPDATE product SET item_pattern = '3D' WHERE item_pattern LIKE '%3d%';
UPDATE product SET item_pattern = 'Flag' WHERE item_pattern LIKE '%flag%';
UPDATE product SET item_pattern = 'Print' WHERE item_pattern LIKE '%print%';
UPDATE product SET item_pattern = 'Geometric' WHERE item_pattern LIKE '%geom%';
UPDATE product SET item_pattern = 'Cartoon' WHERE item_pattern LIKE '%cart%';
UPDATE product SET item_pattern = 'Skeleton' WHERE item_pattern LIKE '%skel%';
UPDATE product SET item_pattern = 'Multiple' WHERE item_pattern LIKE '%patter%';
UPDATE product SET item_pattern = 'Multiple' WHERE item_pattern NOT IN ('Solid','Patchwork','Patchwork','Flowers','Flowers','Stripes','Skull','Animal','3D','Flag','Print','Geometric','Cartoon','Skeleton','Multiple');

UPDATE product SET item_style = 'Hot' WHERE item_style LIKE '%sex%';
UPDATE product SET item_style = 'Sporty' WHERE item_style LIKE '%sport%';
UPDATE product SET item_style = 'Office' WHERE item_style LIKE '%office%';
UPDATE product SET item_style = 'Fashion' WHERE item_style LIKE '%fashion%';
UPDATE product SET item_style = 'Casual' WHERE item_style LIKE '%Casual%';
UPDATE product SET item_style = 'Casual' WHERE item_style NOT IN ('Hot','Sporty','Office','Fashion','Casual');

UPDATE product SET regular_price = (SELECT regular_price FROM product AS prev WHERE regular_price IS NOT '' and prev.rowid < product.rowid order by prev.rowid DESC LIMIT 1) WHERE regular_price IS '' AND price IS '';
"""