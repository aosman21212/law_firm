{
 'name': 'Law Firm Management',
 'version': '18.0.1.0.0',
 'category': 'Services/Legal',
 'summary': 'Manage legal cases, clients, hearings, courts and lawyers',
 'description': """
Law Firm Management
===================
* Legal cases with automatic reference numbers
* Clients, lawyers and case teams
* Courts and case types
* Hearings with calendar view
* Security groups: Law User / Law Manager
""",
 'author': 'Leapai AI',
 'website': 'https://leapai.ai/',
 'license': 'LGPL-3',
 'depends': ['base', 'mail'],
 'data': [
 'security/law_firm_security.xml',
 'security/ir.model.access.csv',
 'data/law_firm_sequence.xml',
 'data/law_case_type_data.xml',
 'views/law_case_views.xml',
 'views/law_hearing_views.xml',
 'views/law_config_views.xml',
 'views/res_partner_views.xml',
 'views/law_firm_menus.xml',
 ],
 'demo': [
 'demo/law_firm_demo.xml',
 ],
 'application': True,
 'installable': True,
}
