from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from datetime import datetime
from datetime import timedelta
import logging
_logger = logging.getLogger(__name__)

class gas_maintenance_vehicle(models.Model):
    _name = 'gas.maintenance.vehicle'
    
    @api.model
    def create(self, values):
        res = super(gas_maintenance_vehicle,self).create(values)
        for rec in res:
            nama = rec.no_ba_o
            if nama == 'New':
                names = self.env['ir.sequence'].next_by_code('gas.maintenance.vehicle')
                rec.update({'no_ba_o':names})    
        return res
            
    def open_records(self):
        ctx = dict(self._context)
        ctx.update({'search_gas_default_vehicle_id': self.id})
        action = self.env['ir.actions.act_window'].for_xml_id('pms_module', 'act_job_crew_3_record_all')
        return dict(action, context=ctx)
    
    no_ba_o = fields.Char(string="No Berita Acara" , default="New")
    tanggal_kerusakan = fields.Date(string="Tanggal Kerusakan", required=False, readonly=False, select=True, default=lambda self: fields.datetime.now())                                                                
    pelapor = fields.Char(string="Pelapor")
    vehicle_id = fields.Many2one(
        'vehicle.vehicle',
        string='Vehicle',
        readonly=False,
        required=False, default=lambda self: self.env.context.get('gas_default_vehicle_id'),
        index=True, tracking=True, change_default=True)
    
    
    catatan = fields.Char(string="Catatan")
    status = fields.Selection(
        string='Status',
        selection=[('open', 'Open'),
                   ('progress', 'Progress'), 
                   ('finish', 'Finish') ],
        default='open',
        store=True,
        readonly=False,
    )
    
    jenis_sarfas = fields.Char(string="Jenis Sarfas")
    nama_sarfas = fields.Char(string="Nama Sarfas")
    uraian_pekerjaan = fields.Char(string="Uraian Pekerjaan")
    
    jenis_downtime = fields.Char(string="Jenis Downtime")
    type_downtime = fields.Char(string="Type Downtime")
    start_perbaikan = fields.Date(string="Start Perbaikan")
    finish_perbaikan = fields.Date(string="Finish Perbaikan")
    
    km = fields.Char(string="Km")
    standar_lama = fields.Char(string="Standar Lama")
    biaya_perbaikan = fields.Char(string="Biaya Perbaikan")
    vendor = fields.Char(string="Vendor")

    
    
    