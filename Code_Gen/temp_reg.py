class TempReg:
  def __init__(self):
    self.init_scatch_table()
    
    
  def init_scatch_table(self):
    scratch_table = [
      {'name': '', 'in_use': False}
    ]
    self.table = scratch_table