from plx_gpib_ethernet import PrologixGPIBEthernetDevice
from time import sleep


class SR760Device(PrologixGPIBEthernetDevice):
    SPAN_FREQS = [191e-3, 382e-3, 763e-3, 1.5, 3.1, 6.1, 12.2, 24.4, 48.75,
                  97.5, 195, 390, 780, 1.56e3, 3.125e3, 6.25e3, 12.5e3, 25e3,
                  50e3, 100e3]
    NUM_BINS = 400
    QUERY_SLEEP = 0.1

    def query(self, cmd, buffer_size=1024*1024):
        self.write(cmd)
        sleep(self.QUERY_SLEEP)
        return self.read(buffer_size)

    def fast_query(self, cmd, buffer_size=1024*1024):
        self.write(cmd)
        return self.read(buffer_size)

    def start(self):
        self.write('STRT')

    def pause(self):
        self.write('STCO')

    def get_unit(self, trace=0):
        i = int( self.query('UNIT? %i' % trace) )
        return self.int_to_unit(i)

    def set_unit(self, u, trace=0):
        self.write( 'UNIT %s,%i' % ( trace, self.unit_to_int(u)) )

    def get_meas_type(self, trace=0):
        i = int( self.query('MEAS? %i' % trace) )
        return self.int_to_meas_type(i)

    def set_meas_type(self, t, trace=0):
        i = self.meas_type_to_int(t)
        self.write( 'MEAS %i,%s' (trace, i) )

    def get_start_freq(self):
        return self._get_freq('STRF')

    def set_start_freq(self, freq):
        self._set_freq('STRF', freq)

    def get_center_freq(self):
        return self._get_freq('CTRF')

    def set_center_freq(self, freq):
        self._set_freq('CTRF', freq)

    def get_span(self):
        i = int( self.query('SPAN?') )
        return self.span_level_to_freq(i)

    def set_span(self, freq):
        l = self.freq_to_span_level(freq)
        self.write('SPAN %i' % l)

    def dump(self, trace=0):
        data = []
        for i in range(SR760Device.NUM_BINS):
            data.append( self._dump_bin(trace, i) )

        return data

    def show_message(self, message):
        self.write('MSGS %s' % message)

    def _get_freq(self, cmd):
        v = self.query('%s?' % cmd)
        return float(v)

    def _set_freq(self, cmd, freq):
        self.write( '%s %e' % (cmd, freq) )

    def _dump_bin(self, trace, nbin=0):
        x = float( self.fast_query('BVAL? %i, %i' % (trace, nbin)) )
        y = float( self.fast_query('SPEC? %i, %i' % (trace, nbin)) )

        return [x, y]

    @staticmethod
    def int_to_unit(i):
        if (i == 0):
            return 'VPk'
        elif (i== 1):
            return 'Vrms'
        elif (i == 2):
            return 'dBV'
        elif (i == 3):
            return 'dBVrms'

        return None

    @staticmethod
    def unit_to_int(u):
        if (u == 'VPk'):
            return 0
        elif (u == 'Vrms'):
            return 1
        elif (u == 'dBV'):
            return 2
        elif (u == 'dBVrms'):
            return 3

        return 0

    @staticmethod
    def int_to_meas_type(i):
        if (i == 0):
            return 'Spectrum'
        elif (i == 1):
            return 'PSD'
        elif (i == 2):
            return 'Time'
        elif (i == 3):
            return 'Octave'

        return None

    @staticmethod
    def meas_type_to_int(t):
        if (t == 'Spectrum'):
            return 0
        elif (t == 'PSD'):
            return 1
        elif (t == 'Time'):
            return 2
        elif (t == 'Octave'):
            return 3

        return 0

    @staticmethod
    def span_level_to_freq(l):
        return SR760Device.SPAN_FREQS[l];

    @staticmethod
    def freq_to_span_level(f):
        for i, sf in enumerate(SR760Device.SPAN_FREQS):
            if f <= sf: return i

        return len(SR760Device.SPAN_FREQS) - 1
