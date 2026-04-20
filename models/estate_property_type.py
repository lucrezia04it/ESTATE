from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence"

    name = fields.Char(required=True)
    
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute="_compute_offer_count", string="Offers Count")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
 
    _sql_constraints = [
        ('check_name_unique', 'UNIQUE(name)', 'Il nome deve essere unico'),
    ]