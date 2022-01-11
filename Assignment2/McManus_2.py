# Assignment \#2
## Kevin McManus, student id: 109702479

class star():
    # optional star properties the star object can keep track of
    _starprops = ['ra','dec','distance','radius','mass','teff']
    
    def __init__(self, name, **kwargs):       
        self.name = name # required
        
        #optional properties
        for prop in star._starprops:
            setattr(self, prop, kwargs.pop(prop, None))
       
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
    def SourceNames(self):
        str = [s.name for s in self.SourceList]
        return str
    def LoadStars(self, starslist=None):
        #load up 4 dummy stars
        self.SourceList = [
                star(name='Mintaka', ra='05:32:00.4009', dec='-00:17:56.7424', distance=380, mass=24.0, teff=29500, radius=16.5),
                star(name='Aldebaran', ra='04:35:55.23907', dec='16:30:33.4885', distance=20, mass=1.16, teff=3900, radius=45.1),
                star(name='Rigel', ra='05:14:32.27210', dec='-08:12:05.8981', distance=264, mass=21.0, teff=12100, radius=78.9),
                star(name='Algol', ra='03:08:10.13245', dec='40:57:20.3280', distance=28, mass=3.17, teff=13000, radius=2.73),
        ]
        d = dict([(s.name, s) for s in self.SourceList])
        return d
    
    
# Main Starts Here
if __name__ == '__main__':
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    
    # my favorite stars (source:https://en.wikipedia.org/wiki/<starname> )

    favs = pd.DataFrame([
        ['Mintaka', '05:32:00.4009', '-00:17:56.7424', 380, 24, 29500, 16.5],
        ['Aldebaran', '04:35:55.23907', '16:30:33.4885', 20, 1.16, 3900, 45.1],
        ['Rigel', '05:14:32.27210', '-08:12:05.8981', 264, 21, 12100, 78.9],
        ['Algol', '03:08:10.13245', '40:57:20.3280', 28, 3.17, 13000, 2.73]
        ]  
        , columns = ['StarName', 'ra', 'dec', 'distance', 'mass', 'teff', 'radius']).set_index('StarName')
    
    print('\n *** Favorite Stars')
    print(favs)
    
    
    print('\n\n** Demo of Star object')
    # create an instance of a star
    # Only name is required, other star properties (ra, dec, distance, mass, radius, teff) optional
    print('\n\n** Star object with only name')
    s1 = star('Mintaka')
    print(s1)
    
    print('\n\n** Star object with name and coordinates')
    #instance with only name and coordinates
    s1 = star('Mintaka', ra='05:32:00.4009', dec='-00:17:56.7424')
    print(s1)
 
    print('\n\n** Star object with all properties populated')
    #create an instance, this time with all the goodies
    s1 = star(name='Mintaka', ra='05:32:00.4009', dec='-00:17:56.7424', distance=380, mass=24.0, teff=29500, radius=16.5)
    print(s1)
    
    print('\n\n** star instances for each of the favorites')
    #create instances for each of the favorites
    for s in favs.index:
        print (star(s,**favs.loc[s]))
        
    print('\n\n** mintaka instance from row in favs table')
    #create a mintaka instance from the info that's in the favorites table
    mintaka = star('Mintaka', **favs.loc['Mintaka'])
    print(mintaka)
    
    #like working with dicts?
    #handy function to turn a star into a dict
    print('\n\n** star.to_dict() functionality')
    mintaka_dict = mintaka.to_dict()
    print(mintaka_dict)
    
    print('\n\n** Demo of Information Object')
    
    #create instance of information object
    print('\n\n** Empty info instance')
    inf = Information()
    print(inf)
    
    print('\n\n** Load up the hard coded stars, print returned dict')
    #load up some info about 4 stars
    #for the moment, the loadstars method loads up these hard coded stars; loadstars returns a dict of the stars so loaded.
    sl = inf.LoadStars()
    print(sl)
    
    #look at the Mintaka object within s1, it's a star object
    print('\n\n** Print the mintaka object from the list returned by loadstars')
    print(sl['Mintaka'])
    
    #for which stars do we have info?
    print('\n\n** The sourcenames() method returns list of star names for which we have info')
    print(inf.SourceNames())
    
    print('\n\n** End of Run')