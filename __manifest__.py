{
	'name': 'Estate',
	'version': '1.0',
	'summary': '',
    'description': "",
	'depends': ['base'],
        'data': [
	        'security/security.xml',
			'security/ir.model.access.csv',
			'views/estate_property_type_views.xml',
			'views/estate_property_tag_views.xml',
			'views/estate_property_offer_views.xml',
			'views/estate_property_views.xml',
			'views/estate_menus.xml',
            'views/res_users_views.xml',
			'report/estate_property_reports.xml',
			'report/estate_property_templates.xml',
		],
		
		"demo": [
			"demo/estate_property_demo.xml",
		],
    
	'installable': True,
	'application': True,
	'auto_install': False
 }
