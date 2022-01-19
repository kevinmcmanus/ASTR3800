# Assignment \#2
## Kevin McManus, student id: 109702479

class star():
    # required star properties the star object keeps track of
    _starprops = ['ra','dec','distance','radius','mass','teff']
    
    def __init__(self, name, **kwargs):       
        self.name = name # required
        
        #required properties; will bomb if property not supplied
        for prop in star._starprops:
            setattr(self, prop, kwargs.pop(prop))
       
    def __repr__(self):
        str = f'Star object: name: {self.name}'
        for prop in star._starprops:
            v = getattr(self, prop, None)
            if v is not None:
                str += f', {prop}: {v}'            
        return str
    
    def to_dict(self):
        d = dict([(prop,getattr(self,prop,None)) for prop in ['name']+star._starprops])
        return d


class Information():
    def __init__(self):
        self.SourceList = []
    def __repr__(self):
        return f'Information Object; Source Names: {self.SourceNames()}'
    def __len__(self):
        return len(self.SourceList)

    def SourceNames(self):
        str = [s.name for s in self.SourceList]
        return str

    def LoadStars(self, starslist=None):
        #load up 4 dummy stars
        self.SourceList = [
                Star(name='Mintaka', ra='05:32:00.4009', dec='-00:17:56.7424', distance=380, mass=24.0, teff=29500, radius=16.5),
                Star(name='Aldebaran', ra='04:35:55.23907', dec='16:30:33.4885', distance=20, mass=1.16, teff=3900, radius=45.1),
                Star(name='Rigel', ra='05:14:32.27210', dec='-08:12:05.8981', distance=264, mass=21.0, teff=12100, radius=78.9),
                Star(name='Algol', ra='03:08:10.13245', dec='40:57:20.3280', distance=28, mass=3.17, teff=13000, radius=2.73),
        ]
        #return a dict of stars so loaded
        d = dict([(s.name, s) for s in self.SourceList])
        return d
    