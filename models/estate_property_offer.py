from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError 

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"
    
    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", 
        inverse="_inverse_date_deadline", 
        store=True
    ) 

    property_type_id = fields.Many2one(
        "estate.property.type", 
        related="property_id.property_type_id", 
        string="Property Type", 
        store=True
    )

    sql_constraints = [
        ('check_price','CHECK(price > 0)','Il prezzo deve essere aggiore di 0'),
    ]

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date.date(), days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=7)
    
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
               record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        for record in self:
            # Controllo: esiste già un'offerta accettata per questa proprietà?
            # Cerchiamo tra tutte le offerte della proprietà se ce n'è una con status 'accepted'
            if record.property_id.offer_ids.filtered(lambda o: o.status == 'accepted'):
                raise UserError("Questa proprietà ha già un'offerta accettata! Rifiuta quella esistente prima di procedere.")
                
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
    
    @api.model
    def create(self, vals):
        prop = self.env['estate.property'].browse(vals['property_id'])
        prop.state = 'offer_received'
        return super().create(vals) #per salvare nel database 