import os
import numpy  as np
import tables as tb

from pytest import mark

from .. core.system_of_units_c import units
from .. core.configure         import configure
from .. core.configure         import all as all_events
from .. io                     import dst_io as dio
from .  esmeralda            import esmeralda

@mark.serial
def test_esmeralda_contains_all_tables(KrMC_hdst_filename, config_tmpdir):
    PATH_IN   = KrMC_hdst_filename
    PATH_OUT  = os.path.join(config_tmpdir, "Kr_tracks_with_MC.h5")
    conf      = configure('dummy invisible_cities/config/esmeralda.conf'.split())
    nevt_req  = all_events

    conf.update(dict(files_in        = PATH_IN,
                     file_out        = PATH_OUT,
                     event_range     = nevt_req))

    esmeralda(**conf)

    with tb.open_file(PATH_OUT) as h5out:
        assert "MC"                      in h5out.root
        assert "MC/extents"              in h5out.root
        assert "MC/hits"                 in h5out.root
        assert "MC/particles"            in h5out.root
        assert "PAOLINA"                 in h5out.root
        assert "PAOLINA/Events"          in h5out.root
        assert "PAOLINA/Summary"         in h5out.root
        assert "PAOLINA/Tracks"          in h5out.root
        assert "RECO/Events"             in h5out.root
        assert "Run"                     in h5out.root
        assert "Run/events"              in h5out.root
        assert "Run/runInfo"             in h5out.root
        assert "Filters/NN_select"       in h5out.root
        assert "Filters/paolina_select"  in h5out.root


@mark.serial
def test_esmeralda_filters_events(KrMC_hdst_filename, config_tmpdir):
    PATH_IN   = KrMC_hdst_filename
    PATH_OUT  = os.path.join(config_tmpdir, "Kr_tracks_with_MC_filtered.h5")
    conf      = configure('dummy invisible_cities/config/esmeralda.conf'.split())
    nevt_req  = 8

    conf.update(dict(files_in              = PATH_IN                                                      ,
                     file_out              = PATH_OUT                                                     ,
                     event_range           = nevt_req)                                                    ,
                     cor_hits_params_NN    = dict(
                         map_fname         = '$ICDIR/database/test_data/kr_emap_xy_100_100_r_6573_time.h5',
                         threshold_charge  = 150  * units.pes                                             ,
                         same_peak         = True                                                         ,
                         apply_temp        = True)                                                        ,
                     cor_hits_params_PL    = dict(
                         map_fname         = '$ICDIR/database/test_data/kr_emap_xy_100_100_r_6573_time.h5',
                         threshold_charge  = 200 * units.pes                                              ,
                         same_peak         = True                                                         ,
                         apply_temp        = True)                                                        )
    cnt = esmeralda(**conf)

    events_pass_NN      =  [0, 1, 2, 3, 4, 5, 6]
    events_pass_paolina =  [3, 4, 5, 6]
    nevt_in             =  cnt.events_in
    nevt_out            =  cnt.events_out
    assert nevt_req     == nevt_in
    assert nevt_out     == len(set(events_pass_paolina))

    df_hits_NN          =  dio.load_dst(PATH_OUT, 'RECO'   , 'Events')
    df_hits_paolina     =  dio.load_dst(PATH_OUT, 'PAOLINA', 'Events')

    assert set(df_hits_NN     .event.unique()) ==  set(events_pass_NN     )
    assert set(df_hits_paolina.event.unique()) ==  set(events_pass_paolina)
