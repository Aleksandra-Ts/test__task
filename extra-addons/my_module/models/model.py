import random
from odoo import models, fields, api, exceptions

class MyNewEntity(models.Model):
    _name = 'my.new.entity'
    _description = 'My New Entity'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name', required=True, readonly=False)
    description = fields.Text(string='Description')
    age = fields.Integer(string='Age')
    active = fields.Boolean(string='Active', default=True)
    date_created = fields.Datetime(string='Date Created', default=fields.Datetime.now)
    amount = fields.Float(string='Amount', digits=(10, 2))
    percentage = fields.Float(string='Percentage', digits=(5, 2))
    selection_field = fields.Selection(
        selection=[('red', 'Red'), ('blue', 'Blue'), ('green', 'Green'),
                   ('black', 'Black'), ('white', 'White')],
        string='Color State',
        required=True
    )
    image = fields.Binary(string='Image')
    file = fields.Binary(string='File')
    url = fields.Char(string='Website URL')
    email = fields.Char(string='Email Address')
    phone = fields.Char(string='Phone Number')
    note = fields.Text(string='Notes')
    user_identifier = fields.Char(string='User Identifier', required=True)
    create_uid = fields.Integer(string='User Id')
    show_change_color_button = fields.Boolean(string='Show Change Color Button', default=False)
    is_user = fields.Boolean(string='Is User', compute='_compute_is_user')

    @api.depends('date_created')
    def _compute_is_user(self):
        for record in self:
            record.is_user = self.env.user.has_group('my_module.group_my_new_entity_user')

    @api.model
    def create(self, vals):
        if 'user_identifier' not in vals:
            vals['user_identifier'] = self.env.user.login
            vals['create_uid'] = self.env.user.id
            
        return super(MyNewEntity, self).create(vals)

    def change_color(self):
        for record in self:
            colors = ['red', 'blue', 'green', 'black', 'white']
            new_color = random.choice(colors)
            record.selection_field = new_color
            record.message_post(body=f'Color changed to {new_color}')
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Color changed successfully!',
                    'type': 'rainbow_man',
                }
            }
        
    def assign_groups(self):
        manager_group = self.env.ref('my_module.group_my_new_entity_manager', raise_if_not_found=False)
        admin_group = self.env.ref('my_module.group_my_new_entity_admin', raise_if_not_found=False)
        user_group = self.env.ref('my_module.group_my_new_entity_user', raise_if_not_found=False)

        users = self.env['res.users'].search([])

        for user in users:
            user.write({'groups_id': [(3, manager_group.id if manager_group else False),
                                    (3, admin_group.id if admin_group else False),
                                    (3, user_group.id if user_group else False)]})

            if user.login == "demo":
                if manager_group:
                    user.write({'groups_id': [(4, manager_group.id)]})
            elif user.login == 'admin':
                if admin_group:
                    user.write({'groups_id': [(4, admin_group.id)]})
            else:
                if user_group:
                    user.write({'groups_id': [(4, user_group.id)]})

        for user in users:
            print(f"User {user.name} is in groups: {user.groups_id.mapped('name')}")
    

    def open_record(self):
        for record in self:
            if record.user_identifier != self.env.user.login and not self.env.user.has_group('my_module.group_my_new_entity_admin'):
                raise exceptions.AccessError("You can only open your own records.")
        return {
            'type': 'ir.actions.act_window',
            'name': 'My New Entity',
            'res_model': 'my.new.entity',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'inline',
            'context': {'form_view_initial_mode': 'edit', 'active_id': self.id},  
        }

    @api.model
    def write(self, vals):
        for record in self:
            if record.user_identifier != self.env.user.login and not self.env.user.has_group('my_module.group_my_new_entity_admin'):
                raise exceptions.AccessError("You can only edit your own records")
        return super(MyNewEntity, self).write(vals)

    @api.model
    def unlink(self):
        for record in self:
            if record.user_identifier != self.env.user.login and not self.env.user.has_group('my_module.group_my_new_entity_admin'):
                raise exceptions.AccessError("You can only delete your own records")
        return super(MyNewEntity, self).unlink()
    
