from odoo import models, fields, api, _

class QATestCase(models.Model):
    _name = 'qa.test.case'
    _description = 'QA Test Case'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Title', compute='_compute_name', store=True)
    tc_id = fields.Char(string='Test Case ID', required=True, copy=False, readonly=True, default=lambda self: _('New'), tracking=True)
    project_id = fields.Many2one('qa.project', string='Project', required=True, tracking=True)
    module_id = fields.Many2one('qa.module', string='Module', domain="[('project_id', '=', project_id)]", required=True, tracking=True)
    section = fields.Char(string='Section / Function')
    
    scenario = fields.Text(string='Test Scenario', required=True)
    pre_condition = fields.Text(string='Pre-Condition')
    test_steps = fields.Text(string='Test Steps', required=True)
    test_data = fields.Text(string='Test Data')
    expected_result = fields.Text(string='Expected Result', required=True)
    actual_result = fields.Text(string='Actual Result')
    
    priority = fields.Selection([
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low')
    ], string='Priority', default='medium', tracking=True)
    
    assigned_tester_id = fields.Many2one('res.users', string='Assigned Tester', tracking=True)
    
    status = fields.Selection([
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('pass', 'Pass'),
        ('fail', 'Fail'),
        ('blocked', 'Blocked'),
        ('skipped', 'Skipped')
    ], string='Status', default='not_started', tracking=True)
    
    testing_type_id = fields.Many2one('qa.testing.type', string='Testing Type')
    
    environment = fields.Selection([
        ('dev', 'Dev'),
        ('staging', 'Staging'),
        ('uat', 'UAT'),
        ('production', 'Production')
    ], string='Environment', default='dev')
    
    build_version = fields.Char(string='Build Version')
    execution_date = fields.Datetime(string='Execution Date', tracking=True)
    notes = fields.Text(string='Notes')
    
    bug_ids = fields.One2many('qa.bug', 'test_case_id', string='Linked Bugs')

    @api.depends('tc_id', 'scenario')
    def _compute_name(self):
        for record in self:
            record.name = f"[{record.tc_id}] {record.scenario[:50]}" if record.scenario else record.tc_id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('tc_id', _('New')) == _('New'):
                # Format: TC-[PROJECT]-[MODULE]-[SEQ]
                seq = self.env['ir.sequence'].next_by_code('qa.test.case.seq') or '0000'
                project = self.env['qa.project'].browse(vals.get('project_id'))
                module = self.env['qa.module'].browse(vals.get('module_id'))
                project_code = project.code if project else 'PROJ'
                module_code = module.code if module else 'MOD'
                vals['tc_id'] = f"TC-{project_code}-{module_code}-{seq}"
        return super(QATestCase, self).create(vals_list)
