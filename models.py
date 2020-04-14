
class N2(db.Model):

    __tablename__ = 'names'
   

    name = db.Column(db.Text,primary_key = True)
    

    def __init__(self,name):
        self.name = name


    def __repr__(self):
        return self.name
