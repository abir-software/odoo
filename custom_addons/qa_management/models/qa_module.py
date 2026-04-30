from odoo import models, fields, api

class QAModule(models.Model):
    _name = 'qa.module'
    _description = 'QA Project Module'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Module Name', required=True, tracking=True)
    code = fields.Char(string='Module Code', required=True, tracking=True)
    project_id = fields.Many2one('qa.project', string='Project', required=True, ondelete='cascade', tracking=True)
    
    priority = fields.Selection([
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low')
    ], string='Priority', default='medium')
    
    testing_type_ids = fields.Many2many('qa.testing.type', string='Testing Types')
    assigned_tester_ids = fields.Many2many('res.users', string='Assigned Testers')
    
    status = fields.Selection([
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('at_risk', 'At Risk'),
        ('completed', 'Completed')
    ], string='Status', default='not_started', tracking=True)
    
    description = fields.Text(string='Description')

class QATestingType(models.Model):
    _name = 'qa.testing.type'
    _description = 'Testing Type'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
