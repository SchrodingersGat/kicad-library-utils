import os, sys

path_to_schlib = os.path.abspath(os.path.join(sys.argv[0],"..","..","schlib"))
sys.path.append(path_to_schlib)
import schlib


class Field:
    def __init__(self, number, text, name="", **kwargs):
        self.number = number
        self.text = text
        self.name = name
        
        self.pos_x = kwargs.get('posx',0)
        self.pos_y = kwargs.get('posy',0)
        self.size = kwargs.get('text_size',50)
        self.orient = kwargs.get('text_orient','H')
        self.visibility = kwargs.get('visibility','V')
        self.hjust = kwargs.get('htext_justify','C')
        self.vjust = kwargs.get('vtext_justify','CNN')
        
    def toString(self):
        return 'F{n} "{txt}" {x} {y} {sz} {o} {v} {hj} {vj}{name}'.format(
            n = self.number,
            txt = self.text,
            x = self.pos_x,
            y = self.pos_x,
            sz = self.size,
            o = self.orient,
            v = self.visibility,
            hj = self.hjust,
            vj = self.vjust,
            name = "" if self.name == "" else " " + self.name
            )
        
#component description
class Description:
    
    def __init__(self, name, description="", keywords="", datasheet=""):
        self.name = name
        self.description = description
        self.keywords = keywords
        self.datasheet = datasheet
        
    def __eq__(self, other):
        return self.name.lower() == other.name.lower()
        
    def toString(self, lf="\n"):
        cmp = []
        cmp.append("#")
        cmp.append("$CMP {name}".format(name=self.name))
        cmp.append("D {desc}".format(desc=self.description))
        cmp.append("K {key}".format(key=self.keywords))
        cmp.append("F {data}".format(data=self.datasheet))
        cmp.append("$ENDCMP" + lf)
        
        return lf.join(cmp)
        
    def alias(self, name):
        if name == self.name:
            return self
            
        d = Description(name, description=self.description, keywords=self.keywords, datasheet=self.datasheet)
            
        return d
            
class Component:
    def __init__(self, description, **kwargs):
        if type(description) is not Description:
            raise TypeError("<description> must be of type 'Description'")
        
        self.designator = kwargs.get('ref','U')
        self.description = description
        self.aliases = []
        self.kwargs = kwargs
        self.fplist = []
        self.fields = []
        self.footprint = kwargs.get('footrint',None)
       
        self.ref_text = Field(0, self.designator)
        self.title_text = Field(1,description.name)
        self.fp_text = Field(2,kwargs.get("footprint",""))
        self.ds_text = Field(3,kwargs.get("datasheet",""))
        
    def addAlias(self, alias):
        if type(alias) is not Description:
            raise TypeError("<alias> must be of type 'Description'")
            
        if alias in self.aliases:
            raise ValueEror("ALIASES must be unique - " + alias.name + " already appears")
            
        #copy over blank data
        if alias.description == "":
            alias.description = self.description.description
        if alias.keywords == "":
            alias.keywords = self.description.keywords
        if alias.datasheet == "":
            alias.datasheet = self.description.datasheet
            
        self.aliases.append(alias)
        
    def toString(self, lf='\n'):
        cmp = []
        cmp.append("#")
        cmp.append("# {name}".format(name=self.description.name))
        cmp.append("#")
        cmp.append("DEF {name} {ref} 0 {to} {dnumber} {dname} {units} {locked} {option}".format(
            name = self.description.name,
            ref = self.designator,
            to = self.kwargs.get('text_offset',40),
            dnumber = self.kwargs.get('draw_pinnumber','Y'),
            dname = self.kwargs.get('draw_pinname','Y'),
            units = self.kwargs.get('unit_count',1),
            locked = self.kwargs.get('units_locked','F'),
            option = self.kwargs.get('option','N')))
        
        #Text fields
        cmp.append(self.ref_text.toString())
        cmp.append(self.title_text.toString())
        cmp.append(self.fp_text.toString())
        cmp.append(self.ds_text.toString())
        
        #aliases
        if len(self.aliases) > 0:
            cmp.append("ALIAS " + " ".join([a.name for a in self.aliases]))
        
        #Footprint list
        if len(self.fplist) > 0:
            cmp.append("$FPLIST")
            
            for f in self.fplist:
                cmp.append(" " + fp)
                
            cmp.append("$ENDFPLIST")
            
        #draw
        cmp.append("DRAW")
        
        #do draw
        
        cmp.append("ENDDRAW")
        cmp.append("ENDDEF")
        
        return lf.join(cmp) + lf

class DeviceLib:
    
    LIB_HEADER = "EESchema-LIBRARY Version 2.3"
    LIB_FOOTER = "#End Library"
    
    DCM_HEADER = "EESchema-DOCLIB  Version 2.0"
    DCM_FOOTER = "#End Doc Library"
    
    def __init__(self, name):
        self.name = name
        self.components = []
        
    def addComponent(self, component):
        if type(component) is not Component:
            raise TypeError("<component> must be of type 'Component'")
            
        self.components.append(component)
        
    def save(self, directory=None, lf='\n'):
        self.saveLib(directory, lf)
        self.saveDcm(directory, lf)
        
    def saveLib(self, directory=None, lf='\n'):
        path = self.name + ".lib"
        if directory:
            path = os.path.abspath(os.path.join(directory, path))
            
        with open(path,'w') as libfile:
            libfile.write(self.LIB_HEADER + lf)
            components = sorted(self.components, key=lambda c: c.description.name)
            for cmp in components:
                libfile.write(cmp.toString())
            libfile.write(self.LIB_FOOTER + lf)
            
    def saveDcm(self, directory=None, lf='\n'):
        path = self.name + ".dcm"
        if directory:
            path = os.path.abspath(os.path.join(directory, path))
            
        with open(path,'w') as dcmfile:
            dcmfile.write(self.DCM_HEADER + lf)
            
            cmp = []
            
            for c in self.components:
                cmp.append(c.description)
                for a in c.aliases:
                    cmp.append(a)
                    
            descriptions = sorted(cmp, key=lambda c: c.name)
            
            for d in descriptions:
                dcmfile.write(d.toString())
            
            dcmfile.write(self.DCM_FOOTER + lf)