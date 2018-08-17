"""
my Gadget specific fields
Adapted from https://mail.python.org/mm3/archives/list/yt-users@python.org/
message/NXCC32FF5IW7DB2PGW2QCLHKH62WLCLJ/

"""

from yt.fields.species_fields import \
    add_species_field_by_density
from yt.frontends.gadget.fields import \
    GadgetFieldInfo
from yt.frontends.sph.fields import \
    SPHFieldInfo

class MyGadgetFieldInfo(GadgetFieldInfo):
    known_particle_fields = (
        ("Mass", ("code_mass", ["particle_mass"], None)),
        ("Masses", ("code_mass", ["particle_mass"], None)),
        ("Coordinates", ("code_length", ["particle_position"], None)),
        ("Velocity", ("code_velocity", ["particle_velocity"], None)),
        ("Velocities", ("code_velocity", ["particle_velocity"], None)),
        ("ParticleIDs", ("", ["particle_index"], None)),
        ("InternalEnergy", ("code_velocity ** 2", ["thermal_energy"], None)),
        ("SmoothingLength", ("code_length", ["smoothing_length"], None)),
        ("Density", ("code_mass / code_length**3", ["density"], None)),
        ("Temperature", ("K", ["temperature"], None)),

        #("Metals", ("code_metallicity", ["metallicity"], None)),
        #("Metallicity", ("code_metallicity", ["metallicity"], None)),
        ("Metallicity_00", ("code_mass", ["He_mass"], None)),
        ("Metallicity_01", ("code_mass", ["C_mass"], None)),
        ("Metallicity_02", ("code_mass", ["Mg_mass"], None)),
        ("Metallicity_03", ("code_mass", ["O_mass"], None)),
        ("Metallicity_04", ("code_mass", ["Fe_mass"], None)),
        ("Metallicity_05", ("code_mass", ["Si_mass"], None)),
        ("Metallicity_06", ("code_mass", ["H_mass"], None)),
        ("Metallicity_07", ("code_mass", ["N_mass"], None)),
        ("Metallicity_08", ("code_mass", ["Ne_mass"], None)),
        ("Metallicity_09", ("code_mass", ["S_mass"], None)),
        ("Metallicity_10", ("code_mass", ["Ca_mass"], None)),
        ("Metallicity_11", ("code_mass", ["rest_mass"], None)),
    )

    def __init__(self, *args, **kwargs):
        super(SPHFieldInfo, self).__init__(*args, **kwargs)
        if ("Gas", "Metallicity_00") in self.field_list:
            self.nuclei_names = ["He", "C", "Mg", "O", "Fe", "Si", "H", "N",
                                 "Ne", "S", "Ca", "rest"]

    def setup_gas_particle_fields(self, ptype):
        super(MyGadgetFieldInfo, self).setup_gas_particle_fields(ptype)

        self.alias((ptype, "temperature"), (ptype, "Temperature"))


        def _metal_mass(field, data):
            return sum( data[(ptype, "%s_mass"%el)]
                    for el in self.nuclei_names if el not in ["H","He"] )
        self.add_field(
            (ptype, "metal_mass"),
            function=_metal_mass,
            sampling_type='particle', # changed to updated yt version
            units="code_mass")


        def _metallicity(field, data):
            return data[(ptype,"metal_mass")] / data[(ptype,"particle_mass")]
        self.add_field(
            (ptype, "metallicity"),
            function=_metallicity,
            sampling_type='particle', # changed to updated yt version
            units="code_metallicity")
            #units="1")#self.ds.unit_system["code_metallicity"])
