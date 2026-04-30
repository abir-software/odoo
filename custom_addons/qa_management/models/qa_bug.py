from odoo import models, fields, api, _

class QABug(models.Model):
    _name = 'qa.bug'
    _description = 'QA Bug'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Title', compute='_compute_name', store=True)
    bug_id = fields.Char(string='Bug ID', required=True, copy=False, readonly=True, default=lambda self: _('New'), tracking=True)
    
    project_id = fields.Many2one('qa.project', string='Project', required=True, tracking=True)
    module_id = fields.Many2one('qa.module', string='Module', domain="[('project_id', '=', project_id)]", tracking=True)
    test_case_id = fields.Many2one('qa.test.case', string='Test Case', domain="[('module_id', '=', module_id)]")
    
    title = fields.Char(string='Bug Title', required=True, tracking=True)
    section_function = fields.Char(string='Section / Function')
    steps_to_reproduce = fields.Text(string='Steps to Reproduce', required=True)
    test_data = fields.Text(string='Test Data')
    expected_result = fields.Text(string='Expected Result', required=True)
    actual_result = fields.Text(string='Actual Result', required=True)
    
    severity = fields.Selection([
        ('critical', 'Critical'),
        ('major', 'Major'),
        ('moderate', 'Moderate'),
        ('minor', 'Minor')
    ], string='Severity', default='moderate', tracking=True)
    
    priority = fields.Selection([
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low')
    ], string='Priority', default='medium', tracking=True)
    
    status = fields.Selection([
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('fixed', 'Fixed'),
        ('retest', 'Re-Test'),
        ('closed', 'Closed'),
        ('rejected', 'Rejected'),
        ('deferred', 'Deferred')
    ], string='Status', default='open', tracking=True)
    
    assigned_developer_id = fields.Many2one('res.users', string='Assigned Developer', tracking=True)
    reported_by_id = fields.Many2one('res.users', string='Reported By', default=lambda self: self.env.user, tracking=True)
    
    reported_date = fields.Datetime(string='Reported Date', default=fields.Datetime.now, readonly=True)
    fixed_date = fields.Datetime(string='Fixed Date', tracking=True)
    closed_date = fields.Datetime(string='Closed Date', tracking=True)
    
    environment = fields.Selection([
        ('dev', 'Dev'),
        ('staging', 'Staging'),
        ('uat', 'UAT')
    ], string='Environment', default='dev')
    
    build_version = fields.Char(string='Build Version')
    dev_comments = fields.Text(string='Developer Comments')
    qa_comments = fields.Text(string='QA Comments')

    @api.depends('bug_id', 'title')
    def _compute_name(self):
        for record in self:
            record.name = f"[{record.bug_id}] {record.title}" if record.title else record.bug_id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('bug_id', _('New')) == _('New'):
                # Format: BG-[PROJECT]-[SEQ]
                seq = self.env['ir.sequence'].next_by_code('qa.bug.seq') or '0000'
                project = self.env['qa.project'].browse(vals.get('project_id'))
                project_code = project.code if project else 'PROJ'
                vals['bug_id'] = f"BG-{project_code}-{seq}"
        return super(QABug, self).create(vals_list)
