from database.tables.base_objects import *
from database.tables import *
import dateparser
import datetime

class Kills(Base, table_row):
    __tablename__ = 'kills'

    kill_id = Column(Integer,primary_key=True, nullable=False, autoincrement=False)
    killmail_time = Column(DateTime,default=None,nullable=True)
    solar_system_id = Column(Integer, ForeignKey(tb_systems.system_id), default=None, nullable=True)
    locationID = Column(Integer,default=None,nullable=True)
    hash = Column(String,default=None,nullable=True)
    fittedValue = Column(Float,default=0.0,nullable=False)
    totalValue = Column(Float,default=0.0,nullable=False)
    points = Column(Float,default=0.0,nullable=False)
    npc = Column(Boolean,default=False,nullable=False)
    solo = Column(Boolean,default=False,nullable=False)
    awox = Column(Boolean, default=False,nullable=False)
    href = Column(String,default=None,nullable=True)
    loaded_time = Column(DateTime,default=datetime.datetime.utcnow(),nullable=False)

    object_system = relationship("Systems", uselist=False, back_populates="object_kills_in_system",lazy="joined")
    object_attackers = relationship("Attackers",uselist=True,back_populates="object_kill",lazy="joined")
    object_victim = relationship("Victims",uselist=False,back_populates="object_kill",lazy="joined")

    def __init__(self, data: dict):
        self.kill_id = data.get("killID")
        killmail_dict = data.get("killmail")
        if killmail_dict:
            self.killmail_time = dateparser.parse(killmail_dict.get("killmail_time"))
            self.solar_system_id = killmail_dict.get("solar_system_id")
        zkb_dict = data.get("zkb")
        if zkb_dict:
            self.locationID = zkb_dict.get("locationID")
            self.hash = zkb_dict.get("hash")
            self.fittedValue = zkb_dict.get("fittedValue")
            self.totalValue = zkb_dict.get("totalValue")
            self.points = zkb_dict.get("points")
            self.npc = zkb_dict.get("npc")
            self.solo = zkb_dict.get("solo")
            self.awox = zkb_dict.get("awox")
            self.href = zkb_dict.get("href")
        self.dict_attackers = killmail_dict.get("attackers") if killmail_dict else None
        self.dict_victim = killmail_dict.get("victim") if killmail_dict else None
        self.loaded_time = datetime.datetime.utcnow()

    def load_fk_objects(self):
        if self.solar_system_id:
            self.object_system = tb_systems(self.solar_system_id)
        if self.dict_attackers:
            for attacker in self.dict_attackers:
                self.object_attackers.append(tb_attackers(attacker))
        if self.dict_victim:
            self.object_victim = tb_victims(self.dict_victim)

    @classmethod
    def primary_key_row(cls):
        return cls.kill_id

    @classmethod
    def make_row(cls, data, service_module):
        id = data.get("killID")
        if id:
            db: Session = service_module.get_session()
            try:
                __row = db.query(cls).filter(cls.primary_key_row() == id).one()
                return None
            except NoResultFound:
                __row = cls(data)
                __row.load_fk_objects()
                service_module.get_session().merge(__row)
                return __row
        else:
            return None

    @classmethod
    def get_row(cls, data, service_module):
        db:Session = service_module.get_session()
        return db.query(cls).filter(cls.primary_key_row() == data.get("killID")).one()

