Odoo CSV Import Export Library
==============================
This library provides tools to easily and quickly import data into Odoo or export data from Odoo using CSV file. 
It also provide a framework to manipulate date from csv.

Requirements
--------------
* openerp-client-lib

Tips
----

* Before import any data with this library, test between five and ten lines of your csv file with the Odoo wizard, to make it sure work.
* To increase performance, set your Odoo to run with workers. More information in https://www.odoo.com/documentation/10.0/setup/deploy.html
* To more informations about how to import large data into Odoo, access https://www.odoo.com/pt_BR/slides/slide/how-to-import-large-complex-data-into-odoo-455/pdf_content

How to use
-------------
**Using terminal**::
 
 $ git clone https://github.com/Trust-Code/odoo_csv_import.git
 $ cd odoo_csv_import
 $ pip install -R requirement.txt
 $ python setup.py install
 $ edit connection.config

**Basic command to import**::

$ odoo_import_thread.py -c {{connection.conf}} --file {{file.csv}} --model {{odoo_model}}

**Parameters**::

-c or --config - default="conf/connection.conf" - Configuration File that contains connection parameters - required = True
--file - File to import - required = True
--model - Model to import - required = True
--worker - default=1 - Number of simultaneous connection
--size - default=10 - Number of line to import per connection
--skip - default=0 - Skip until line [SKIP]
--fail - Fail mode
-s or --sep - default=";" - CSV separator
--groupby - Group data per batch with the same value for the given column in order to avoid concurrent update error
--ignore - list of column separate by comma. Those column will be remove from the import request
--check - Check if record are imported after each batch.
--context - default="{'tracking_disable' : True}" - context that will be passed to the load function, need to be a valid python dict'