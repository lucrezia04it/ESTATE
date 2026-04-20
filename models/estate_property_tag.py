from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    name = fields.Char(required=True)
    color = fields.Integer("Color")
    
    _sql_constraints =[
        ('check_name_unique', 'UNIQUE(name)', 'Il nome deve essere unico'),
    ]