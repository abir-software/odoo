from odoo import models, fields, api

class QAProject(models.Model):
    _name = 'qa.project'
    _description = 'QA Project'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    odoo_project_id = fields.Many2one('project.project', string='Linked Project', required=True, tracking=True)
    name = fields.Char(string='Project Name', related='odoo_project_id.name', store=True, readonly=False, tracking=True)
    code = fields.Char(string='Project Code', required=True, copy=False, tracking=True)
    client_name = fields.Char(string='Client / Department')
    project_manager_id = fields.Many2one('res.users', string='Project Manager', related='odoo_project_id.user_id', store=True, readonly=False, tracking=True)
    qa_lead_id = fields.Many2one('res.users', string='QA Lead', tracking=True)
    
    @api.onchange('odoo_project_id')
    def _onchange_odoo_project_id(self):
        if self.odoo_project_id and not self.code:
            words = self.odoo_project_id.name.split()
            code = "".join([w[0].upper() for w in words if w[0].isalnum()])
            self.code = code
    start_date = fields.Date(string='Start Date')
    target_go_live_date = fields.Date(string='Target Go-Live Date')
    
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('on_hold', 'On Hold'),
        ('uat', 'UAT'),
        ('ready', 'Ready for Go-Live'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    
    description = fields.Text(string='Description')
    module_ids = fields.One2many('qa.module', 'project_id', string='Modules')
    
    module_count = fields.Integer(compute='_compute_counters', string='Modules Count')
    test_case_count = fields.Integer(compute='_compute_counters', string='Test Cases Count')
    bug_count = fields.Integer(compute='_compute_counters', string='Bugs Count')
    
    def _compute_counters(self):
        for project in self:
            project.module_count = self.env['qa.module'].search_count([('project_id', '=', project.id)])
            project.test_case_count = self.env['qa.test.case'].search_count([('project_id', '=', project.id)])
            project.bug_count = self.env['qa.bug'].search_count([('project_id', '=', project.id)])
            
    def action_view_modules(self):
        return {
            'name': 'Modules',
            'res_model': 'qa.module',
            'view_mode': 'list,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
            'type': 'ir.actions.act_window',
        }

    def action_view_test_cases(self):
        return {
            'name': 'Test Cases',
            'res_model': 'qa.test.case',
            'view_mode': 'list,form,graph',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
            'type': 'ir.actions.act_window',
        }

    def action_view_bugs(self):
        return {
            'name': 'Bugs',
            'res_model': 'qa.bug',
            'view_mode': 'list,form,graph',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
            'type': 'ir.actions.act_window',
        }
