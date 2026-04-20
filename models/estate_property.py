from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"
    
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    color = fields.Integer("Color")
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ]
    )
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
        ('new', 'New'),
        ('offer_received', 'Offerta ricevuta'),
        ('offer_accepted', 'In Trattativa'), 
        ('venduto', 'Venduto'),
        ('cancelled', 'Cancellato'),
    ],
        required=True,
        copy=False,
        default='new',
    )
    image = fields.Image("Foto principale", max_width=1024, max_height=1024)

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'il prezzo deve essere maggiore di 0'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'Il prezzo di vendita deve essere uguale o maggiore di 0'),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
    
    def action_sold(self):
        for record in self:
            if record.state == "cancellato":
                raise UserError("Una proprietà cancellata non può essere venduta.")
        
            record.state = "venduto"
        return True

    def action_cancelled(self):
        for record in self:
            if record.state == "venduto":
                raise UserError("Una proprietà venduta non può essere cancellata")

            record.state = "cancellato"
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            
            if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) == -1:
                raise ValidationError("Il prezzo di vendità non può essere inore del 90% del prezzo previsto! Occhio!")
            
    @api.ondelete(at_uninstall=False)
    def _check_state_before_deletion(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise UserError("Non puoi eliminare una proprietà venduta")