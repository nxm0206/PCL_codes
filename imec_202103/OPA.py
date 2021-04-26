from technologies.si_photonics.picazzo.default import *

from ipkiss.all import *
import numpy as np

from picazzo.wg.taper import WgElTaperShallowDeep,WgElTaperDeepShallow,WgElTaperLinear
from picazzo.fibcoup.socket import LinearTaperSocket
from picazzo.wg.aperture import OpenAperture
from picazzo.fibcoup.socket import OpenApertureSocket
from ipkiss.plugins.photonics.wg.basic import *
from ipkiss.plugins.photonics.wg.definition import WaveguideDefProperty
from ipkiss.plugins.photonics.wg.connect import WaveguidePointRoundedConnectElementDefinition
from ipkiss.plugins.photonics.port import *
from ipkiss.plugins.photonics.routing import *
from picazzo.container import ExtendPorts
from picazzo.filters.mmi import Mmi1x2
from picazzo.fibcoup.uniform import UniformLineGrating
from picazzo.container.taper_ports import TaperDeepPorts


from ipkiss.process import PPLayer, ProcessProperty
from ipkiss.plugins.photonics.wg.basic import WgElDefinition
from ipkiss.plugins.photonics.wg.window import PathWindow, WindowWaveguideDefinition
from picazzo.phc.holes import *
from picazzo.wg.bend import WgElBend
from ipkiss.geometry.shapes.spline import SplineRoundingAlgorithm

from ipkiss.io.input_gdsii import InputGdsii

from picazzo.wg.wgdefs.wg_fc import WGFCWgElDefinition
from picazzo.wg.tapers.auto_taper.auto_taper import WgElPortTaperAuto
from picazzo.wg.spiral import WgSpiralFixedLength
from picazzo.filters.ring import RingRectNotchFilter, RingRect180DropFilter, RingRect90DropFilter, RingRectBentNotchFilter, RingRectBent180DropFilter

from picazzo.wg.sbend import WgElSBend


class Ybranch(Structure):
    __name_prefix__ = 'Ybranch'
    L_in = PositiveNumberProperty(default=1.0)
    L_out = PositiveNumberProperty(default=1.0)
    L_splitter = PositiveNumberProperty(default=2)
    L_bend = PositiveNumberProperty(default=10.0)
    w_port = PositiveNumberProperty(default=0.45)
    w_trench = PositiveNumberProperty(default=2.0)
    w_list = ListProperty(default=[0.45, 0.6, 0.8, 1.2, 1.2, 1.16, 1.14, 1.23, 1.2, 1.18, 1.1, 1.1, 1.1])
    bend_radius = PositiveNumberProperty(default=10.0)
    out_sep = PositiveNumberProperty(default=1.65)
    gap = PositiveNumberProperty(default=0.2)
    min_straight = PositiveNumberProperty(default=1.0)
    # layers
    WGcore = PPLayer(process=TECH.PROCESS.WG, purpose=TECH.PURPOSE.LF.LINE)
    WGclad = PPLayer(process=TECH.PROCESS.WG, purpose=TECH.PURPOSE.LF_AREA)

    def define_elements(self, elems):

        # input waveguide
        elems += Rectangle(layer=self.WGcore, center=(self.L_in/2.0, 0.0),
                           box_size=(self.L_in, self.w_port))
        elems += Rectangle(layer=self.WGclad, center=(self.L_in/2.0, 0.0),
                           box_size=(self.L_in, self.w_port+2.0*self.w_trench))

        # splitter
        N = len(self.w_list)
        L_list = np.linspace(start=self.L_in, stop=self.L_in+self.L_splitter, num=N, endpoint=True)
        pts_core = []
        pts_clad = []
        for i in range(N):
            pts_core.append((L_list[i], self.w_list[i]/2.0))
            pts_clad.append((L_list[i], np.max(self.w_list)/2.0+self.w_trench))
        for i in range(N):
            pts_core.append((L_list[N-i-1], -self.w_list[N-i-1]/2.0))
            pts_clad.append((L_list[N-i-1], -np.max(self.w_list)/2.0 - self.w_trench))

        # print pts_core
        elems += Boundary(layer=self.WGcore, shape=Shape(points=pts_core))
        elems += Boundary(layer=self.WGclad, shape=Shape(points=pts_clad))

        port1 = OpticalPort(position=(self.L_in+self.L_splitter, self.gap/2.0+self.w_port/2.0), angle=0,
                             wg_definition=WgElDefinition(wg_width=self.w_port, trench_width=self.w_trench))

        port2 = OpticalPort(position=(self.L_in+self.L_splitter, -self.gap/2.0-self.w_port/2.0), angle=0,
                             wg_definition=WgElDefinition(wg_width=self.w_port, trench_width=self.w_trench))

        bend1 = RouteConnectorRounded(RouteToEastAtY(input_port=port1, bend_radius=self.bend_radius, y_position=self.out_sep/2.0,
                             min_straight=self.min_straight))
        bend2 = RouteConnectorRounded(RouteToEastAtY(input_port=port2, bend_radius=self.bend_radius, y_position=-self.out_sep/2.0,
                             min_straight=self.min_straight))
        elems += bend1
        elems += bend2

        # output waveguide
        L_bend1 = bend1.size_info().width
        L_bend2 = bend2.size_info().width

        elems += Rectangle(layer=self.WGclad, center=(self.L_in+self.L_splitter+max([L_bend1, L_bend2])/2.0, 0.0),
                           box_size=(max([L_bend1, L_bend2]), self.out_sep+self.w_port+2.0*self.w_trench))


        elems += Rectangle(layer=self.WGcore, center=(self.L_in+self.L_splitter+L_bend1+self.L_out/2.0, self.out_sep/2.0),
                           box_size=(self.L_out, self.w_port))
        elems += Rectangle(layer=self.WGclad, center=(self.L_in+self.L_splitter+L_bend1+self.L_out/2.0, self.out_sep/2.0),
                           box_size=(self.L_out, self.w_port+2.0*self.w_trench))

        elems += Rectangle(layer=self.WGcore, center=(self.L_in+self.L_splitter+L_bend2+self.L_in/2.0, -self.out_sep/2.0),
                           box_size=(self.L_in, self.w_port))
        elems += Rectangle(layer=self.WGclad, center=(self.L_in+self.L_splitter+L_bend2+self.L_in/2.0, -self.out_sep/2.0),
                           box_size=(self.L_in, self.w_port+2.0*self.w_trench))

        return elems

    def define_ports(self, ports):

        ports += OpticalPort(name="in", position=(0.0, 0.0), angle=180, wg_definition=WgElDefinition(wg_width=self.w_port,
                                                                                           trench_width=self.w_trench))
        ports += OpticalPort(name="out1", position=(self.L_in+self.L_splitter+self.L_bend1, self.out_sep), angle=0, wg_definition=WgElDefinition(wg_width=self.w_port,
                                                                                           trench_width=self.w_trench))
        ports += OpticalPort(name="out2", position=(self.L_in+self.L_splitter+self.L_bend1, -self.out_sep), angle=0, wg_definition=WgElDefinition(wg_width=self.w_port,
                                                                                           trench_width=self.w_trench))

        return ports


class ReceiverElement(Structure):
    __name_prefix__ = 'ReceiverElement'
    LWGetch = PositiveNumberProperty(default=0.65)
    LWGline = PositiveNumberProperty(default=0.2)
    LSKTetch = PositiveNumberProperty(default=0.3)
    LFCetch = PositiveNumberProperty(default=0.45)
    LFCline = PositiveNumberProperty(default=0.55)
    Ltaper = PositiveNumberProperty(default=1.45)
    w_port = PositiveNumberProperty(default=0.45)
    w_trench = PositiveNumberProperty(default=2.0)
    w_w = PositiveNumberProperty(default=2.0)
    L_straight = PositiveNumberProperty(default=5.0)
    resolution = IntProperty(default=20)



    # layers
    WGcore = PPLayer(process=TECH.PROCESS.WG, purpose=TECH.PURPOSE.LF.LINE)
    WGclad = PPLayer(process=TECH.PROCESS.WG, purpose=TECH.PURPOSE.LF_AREA)
    FCcore = PPLayer(process=TECH.PROCESS.FC, purpose=TECH.PURPOSE.LF.LINE)#thickness 140
    FCclad = PPLayer(process=TECH.PROCESS.FC, purpose=TECH.PURPOSE.LF_AREA)
    FCtrench = PPLayer(process=TECH.PROCESS.FC, purpose=TECH.PURPOSE.DF.TRENCH)
    SKTcore = PPLayer(process=TECH.PROCESS.SK, purpose=TECH.PURPOSE.LF.LINE)#thickness 60
    SKTclad = PPLayer(process=TECH.PROCESS.SK, purpose=TECH.PURPOSE.LF_AREA)
    SKTtrench = PPLayer(process=TECH.PROCESS.SK, purpose=TECH.PURPOSE.DF.TRENCH)

    def define_elements(self, elems):

        # input waveguide
        elems += Rectangle(layer=self.WGcore, center=(self.L_straight/2.0, 0.0),
                           box_size=(self.L_straight, self.w_port))
        elems += Rectangle(layer=self.WGclad, center=(self.L_straight/2.0, 0.0),
                           box_size=(self.L_straight, self.w_port+2.0*self.w_trench))

        # splitter
        L_list = np.linspace(start=0.0, stop=self.Ltaper, num=self.resolution, endpoint=True)
        pts_taper = []
        taper_para_a = (self.w_w-self.w_port)/self.Ltaper**2
        taper_para_b = self.w_w
        for i in range(self.resolution):
            pts_taper.append((self.L_straight+self.Ltaper-L_list[i], (taper_para_b-taper_para_a*L_list[i]**2)/2.0))

        for i in range(self.resolution):
            pts_taper.append((self.L_straight+self.Ltaper-L_list[self.resolution-i-1], -(taper_para_b-taper_para_a*L_list[self.resolution-i-1]**2)/2.0))

        # print pts_taper
        # print pts_core
        elems += Boundary(layer=self.WGcore, shape=Shape(points=pts_taper))

        elems += Rectangle(layer=self.WGcore, center=(self.L_straight+self.Ltaper+(self.LFCline+self.LFCetch+self.LSKTetch+self.LWGline)/2.0, 0.0),
                           box_size=((self.LFCline+self.LFCetch+self.LSKTetch+self.LWGline), self.w_w))

        elems += Rectangle(layer=self.FCtrench, center=(self.L_straight+self.Ltaper+self.LFCline+self.LFCetch/2.0, 0.0),
                           box_size=(self.LFCetch, self.w_w+0.2))

        elems += Rectangle(layer=self.SKTtrench, center=(self.L_straight+self.Ltaper+self.LFCline+self.LFCetch+self.LSKTetch/2.0, 0.0),
                           box_size=(self.LSKTetch, self.w_w+0.3))

        elems += Rectangle(layer=self.WGcore, center=(self.L_straight+self.Ltaper+self.LFCline+self.LFCetch+self.LSKTetch+self.LWGline+self.LWGetch+self.LWGline/2.0, 0.0),
                           box_size=(self.LWGline, self.w_w))

        elems += Rectangle(layer=self.WGcore, center=(self.L_straight + self.Ltaper + self.LFCline + self.LFCetch + self.LSKTetch + self.LWGline + self.LWGetch + self.LWGline + self.LWGetch + self.LWGline / 2.0, 0.0), box_size=(self.LWGline, self.w_w))

        elems += Rectangle(layer=self.WGcore, center=(self.L_straight + self.Ltaper + self.LFCline + self.LFCetch + self.LSKTetch + self.LWGline + self.LWGetch + self.LWGline + self.LWGetch + self.LWGline + self.LWGetch + self.LWGline / 2.0,
        0.0), box_size=(self.LWGline, self.w_w))


        elems += Rectangle(layer=self.WGclad, center=(self.L_straight+(self.Ltaper+self.LFCline+self.LFCetch+self.LSKTetch+self.LWGline*4.0+self.LWGetch*3.0+1.0)/2.0, 0.0),
                           box_size=(self.Ltaper+self.LFCline+self.LFCetch+self.LSKTetch+self.LWGline*4.0+self.LWGetch*3.0+1.0, self.w_port+2.0*self.w_trench))



        return elems


class Transition(Structure):
    __name_prefix__ = 'Transition'
    Lwgtaper = PositiveNumberProperty(default=10.2)
    Lwg = PositiveNumberProperty(default=2.0)
    Lsktaper = PositiveNumberProperty(default=20)
    Lsk = PositiveNumberProperty(default=0.2)
    w_sktrench = PositiveNumberProperty(default=0.775)

    wg1 = PositiveNumberProperty(default=0.45)
    wg2 = PositiveNumberProperty(default=0.45)
    wg3 = PositiveNumberProperty(default=1.5)


    w_trench = PositiveNumberProperty(default=2.0)






    def define_elements(self, elems):

        # layers
        WGcore = PPLayer(process=TECH.PROCESS.WG, purpose=TECH.PURPOSE.LF.LINE)
        WGclad = PPLayer(process=TECH.PROCESS.WG, purpose=TECH.PURPOSE.LF_AREA)
        SKcore = PPLayer(process=TECH.PROCESS.SK, purpose=TECH.PURPOSE.LF.LINE)
        SKclad = PPLayer(process=TECH.PROCESS.SK, purpose=TECH.PURPOSE.LF_AREA)

        # input waveguide

        elems += Wedge(layer=SKclad, begin_coord=(0.0,0.0),end_coord=(self.Lsktaper, 0.0),
                       begin_width=self.w_sktrench*2.0+self.wg2, end_width=self.w_trench*2.0+self.wg2)

        elems += Wedge(layer=SKcore, begin_coord=(0.0,0.0), end_coord=(self.Lsktaper, 0.0),
                       begin_width=self.wg2, end_width=self.wg2)

        elems += Wedge(layer=SKclad, begin_coord=(self.Lsktaper,0.0),end_coord=(self.Lsktaper+self.Lsk, 0.0),
                       begin_width=self.w_trench*2.0+self.wg2, end_width=self.w_trench*2.0+self.wg2)

        elems += Wedge(layer=SKcore, begin_coord=(self.Lsktaper,0.0),end_coord=(self.Lsktaper+self.Lsk, 0.0),
                       begin_width=self.wg2, end_width=self.wg2)


        elems += Wedge(layer=WGclad, begin_coord=(self.Lsktaper-self.Lwgtaper,0.0),end_coord=(self.Lsktaper, 0.0),
                       begin_width=self.wg3+self.w_trench*2.0, end_width=self.wg1+self.w_trench*2.0)

        elems += Wedge(layer=WGcore, begin_coord=(self.Lsktaper-self.Lwgtaper,0.0),end_coord=(self.Lsktaper, 0.0),
                       begin_width=self.wg3, end_width=self.wg1)

        elems += Wedge(layer=WGclad, begin_coord=(self.Lsktaper,0.0),end_coord=(self.Lsktaper+self.Lwg, 0.0),
                       begin_width=self.wg1+self.w_trench*2.0, end_width=self.wg1+self.w_trench*2.0)

        elems += Wedge(layer=WGcore, begin_coord=(self.Lsktaper,0.0),end_coord=(self.Lsktaper+self.Lwg, 0.0),
                       begin_width=self.wg1, end_width=self.wg1)

        return elems


class MMI1x2(Structure):
    __name_prefix__ = 'MMI1x2'
    L_in = PositiveNumberProperty(default=1.0)
    L_out = PositiveNumberProperty(default=1.0)
    L_MMI = PositiveNumberProperty(default=8.64)
    L_taper = PositiveNumberProperty(default=10.0)
    ww = PositiveNumberProperty(default=1.2)
    w_port = PositiveNumberProperty(default=0.45)
    w_trench = PositiveNumberProperty(default=2.0)
    w_MMI = PositiveNumberProperty(default=3.15)
    bend_radius = PositiveNumberProperty(default=50.0)
    out_sep = PositiveNumberProperty(default=10.0)
    gap = PositiveNumberProperty(default=0.42)
    min_straight = PositiveNumberProperty(default=1.0)



    # layers
    WGcore = PPLayer(process=TECH.PROCESS.WG, purpose=TECH.PURPOSE.LF.LINE)
    WGclad = PPLayer(process=TECH.PROCESS.WG, purpose=TECH.PURPOSE.LF_AREA)

    def define_elements(self, elems):

        # input waveguide

        elems += SRef(WireTaper(w_start=self.w_port, w_end=self.w_port, taperlen=self.L_in, w_trench=self.w_trench), position=(0.0, 0.0))
        elems += SRef(WireTaper(w_start=self.w_port, w_end=self.ww, taperlen=self.L_taper, w_trench=self.w_trench), position=(self.L_in, 0.0))
        elems += SRef(WireTaper(w_start=self.w_MMI, w_end=self.w_MMI, taperlen=self.L_MMI, w_trench=self.w_trench),
                      position=(self.L_in+self.L_taper, 0.0))
        elems += SRef(WireTaper(w_start=self.ww, w_end=self.w_port, taperlen=self.L_taper, w_trench=self.w_trench),
                      position=(self.L_in+self.L_taper+self.L_MMI, self.gap/2.0+self.ww/2.0))
        elems += SRef(WireTaper(w_start=self.ww, w_end=self.w_port, taperlen=self.L_taper, w_trench=self.w_trench),
                      position=(self.L_in+self.L_taper+self.L_MMI, -self.gap/2.0-self.ww/2.0))




        #bend
        port1 = OpticalPort(position=(self.L_in+self.L_taper*2.0+self.L_MMI, self.gap/2.0+self.ww/2.0), angle=0,
                             wg_definition=WgElDefinition(wg_width=self.w_port, trench_width=self.w_trench))

        port2 = OpticalPort(position=(self.L_in+self.L_taper*2.0+self.L_MMI, -self.gap/2.0-self.ww/2.0), angle=0,
                             wg_definition=WgElDefinition(wg_width=self.w_port, trench_width=self.w_trench))

        bend1 = RouteConnectorRounded(RouteToEastAtY(input_port=port1, bend_radius=self.bend_radius, y_position=self.out_sep/2.0,
                             min_straight=self.min_straight))
        bend2 = RouteConnectorRounded(RouteToEastAtY(input_port=port2, bend_radius=self.bend_radius, y_position=-self.out_sep/2.0,
                             min_straight=self.min_straight))
        elems += bend1
        elems += bend2

        # output waveguide
        L_bend1 = bend1.size_info().width
        L_bend2 = bend2.size_info().width

        if self.out_sep+self.w_port+2.0*self.w_trench -self.w_MMI-self.w_trench*2.0 >= 0:
            w_block = self.out_sep+self.w_port+2.0*self.w_trench
        else:
            w_block = self.w_MMI + self.w_trench * 2.0

        elems += Rectangle(layer=self.WGclad, center=(self.L_in+self.L_taper*2.0+self.L_MMI+(max([L_bend1, L_bend2])-self.L_taper)/2.0, 0.0),
                           box_size=(max([L_bend1, L_bend2])+self.L_taper, w_block))

        elems += SRef(WireTaper(w_start=self.w_port, w_end=self.w_port, taperlen=self.L_out, w_trench=self.w_trench),
                      position=(self.L_in+self.L_taper*2.0+self.L_MMI+L_bend1, self.out_sep/2.0))
        elems += SRef(WireTaper(w_start=self.w_port, w_end=self.w_port, taperlen=self.L_out, w_trench=self.w_trench),
                      position=(self.L_in+self.L_taper*2.0+self.L_MMI+L_bend2, -self.out_sep/2.0))


        return elems

    def define_ports(self, ports):

        ports += OpticalPort(name="in", position=(0.0, 0.0), angle=180, wg_definition=WgElDefinition(wg_width=self.w_port,
                                                                                           trench_width=self.w_trench))
        ports += OpticalPort(name="out1", position=(self.L_in+self.L_taper*2.0+self.L_MMI+self.L_bend1+self.L_out, self.out_sep), angle=0, wg_definition=WgElDefinition(wg_width=self.w_port,
                                                                                           trench_width=self.w_trench))
        ports += OpticalPort(name="out2", position=(self.L_in+self.L_taper*2.0+self.L_MMI+self.L_bend2+self.L_out, -self.out_sep), angle=0, wg_definition=WgElDefinition(wg_width=self.w_port,
                                                                                           trench_width=self.w_trench))

        return ports


class MMI2x2(Structure):
    __name_prefix__ = 'MMI2x2'
    L_in = NumberProperty(default=0.0)
    L_out = PositiveNumberProperty(default=2.019)
    L_MMI = PositiveNumberProperty(default=17.566)
    L_taper = PositiveNumberProperty(default=9.372)
    ww = PositiveNumberProperty(default=1.14)
    w_port = PositiveNumberProperty(default=0.45)
    w_trench = PositiveNumberProperty(default=2.0)
    w_MMI = PositiveNumberProperty(default=3.9)
    bend_radius = PositiveNumberProperty(default=10.0)
    out_sep = PositiveNumberProperty(default=4.0)
    sep = PositiveNumberProperty(default=1.484)
    min_straight = PositiveNumberProperty(default=1.0)



    # layers
    WGcore = PPLayer(process=TECH.PROCESS.WG, purpose=TECH.PURPOSE.LF.LINE)
    WGclad = PPLayer(process=TECH.PROCESS.WG, purpose=TECH.PURPOSE.LF_AREA)

    def define_elements(self, elems):

        wg = WgElDefinition(wg_width=self.w_port, trench_width=self.w_trench)

        # input waveguide

        # elems += SRef(WireTaper(w_start=self.w_port, w_end=self.w_port, taperlen=self.L_in, w_trench=self.w_trench),
        #               position=(0.0, 0.0))
        elems += SRef(WireTaper(w_start=self.w_port, w_end=self.ww, taperlen=self.L_taper, w_trench=self.w_trench),
                      position=(self.L_in, -self.sep/2.0))
        elems += SRef(WireTaper(w_start=self.w_port, w_end=self.ww, taperlen=self.L_taper, w_trench=self.w_trench),
                      position=(self.L_in, self.sep/2.0))

        elems += SRef(WireTaper(w_start=self.w_MMI, w_end=self.w_MMI, taperlen=self.L_MMI, w_trench=self.w_trench),
                      position=(self.L_in+self.L_taper, 0.0))

        elems += SRef(WireTaper(w_start=self.ww, w_end=self.w_port, taperlen=self.L_taper, w_trench=self.w_trench),
                      position=(self.L_in+self.L_taper+self.L_MMI, self.sep/2.0))
        elems += SRef(WireTaper(w_start=self.ww, w_end=self.w_port, taperlen=self.L_taper, w_trench=self.w_trench),
                      position=(self.L_in+self.L_taper+self.L_MMI, -self.sep/2.0))




        #bend
        port3 = OpticalPort(position=(self.L_in+self.L_taper*2.0+self.L_MMI, self.sep/2.0), angle=0,
                             wg_definition=wg)

        port4 = OpticalPort(position=(self.L_in+self.L_taper*2.0+self.L_MMI, -self.sep/2.0), angle=0,
                             wg_definition=wg)

        bend3 = RouteConnectorRounded(RouteToEastAtY(input_port=port3, bend_radius=self.bend_radius, y_position=self.out_sep/2.0,
                             min_straight=self.min_straight))
        bend4 = RouteConnectorRounded(RouteToEastAtY(input_port=port4, bend_radius=self.bend_radius, y_position=-self.out_sep/2.0,
                             min_straight=self.min_straight))
        elems += bend3
        elems += bend4

        elems += bend3.transform_copy(HMirror(mirror_plane_x=0.0)+Translation((self.L_taper*2.0+self.L_MMI, 0.0)))
        elems += bend4.transform_copy(HMirror(mirror_plane_x=0.0)+Translation((self.L_taper*2.0+self.L_MMI, 0.0)))

        # output waveguide
        L_bend3 = bend3.size_info().width
        L_bend4 = bend4.size_info().width

        if self.out_sep+self.w_port+2.0*self.w_trench -self.w_MMI-self.w_trench*2.0 >= 0:
            w_block = self.out_sep+self.w_port+2.0*self.w_trench
        else:
            w_block = self.w_MMI + self.w_trench * 2.0

        elems += Rectangle(layer=self.WGclad, center=(self.L_in+self.L_taper*2.0+self.L_MMI+(max([L_bend3, L_bend4])-self.L_taper)/2.0, 0.0),
                           box_size=(max([L_bend3, L_bend4])+self.L_taper, w_block))

        elems += Rectangle(layer=self.WGclad, center=(self.L_in-(max([L_bend3, L_bend4])-self.L_taper)/2.0, 0.0),
                           box_size=(max([L_bend3, L_bend4])+self.L_taper, w_block))

        elems += SRef(WireTaper(w_start=self.w_port, w_end=self.w_port, taperlen=self.L_out, w_trench=self.w_trench),
                      position=(self.L_in+self.L_taper*2.0+self.L_MMI+L_bend3, self.out_sep/2.0))
        elems += SRef(WireTaper(w_start=self.w_port, w_end=self.w_port, taperlen=self.L_out, w_trench=self.w_trench),
                      position=(self.L_in+self.L_taper*2.0+self.L_MMI+L_bend4, -self.out_sep/2.0))

        elems += SRef(WireTaper(w_start=self.w_port, w_end=self.w_port, taperlen=self.L_out, w_trench=self.w_trench),
                      position=(-L_bend3-self.L_out, self.out_sep/2.0))
        elems += SRef(WireTaper(w_start=self.w_port, w_end=self.w_port, taperlen=self.L_out, w_trench=self.w_trench),
                      position=(-L_bend3-self.L_out, -self.out_sep/2.0))


        return elems


class WireTaper(Structure):
    __name_prefix__ = 'WireTaper'
    taperlen = PositiveNumberProperty(default=20.0)
    w_start = PositiveNumberProperty(default=0.45)
    w_end = PositiveNumberProperty(default=0.45)
    w_trench = PositiveNumberProperty(default=2.0)
    process = ProcessProperty(default=TECH.PROCESS.WG)



    def define_elements(self, elems):
        WGcore = PPLayer(process=self.process, purpose=TECH.PURPOSE.LF.LINE)
        WGclad = PPLayer(process=self.process, purpose=TECH.PURPOSE.LF_AREA)

        elems += Wedge(layer=WGcore, begin_coord=(0.0,0.0),end_coord=(self.taperlen,0.0),
                       begin_width=self.w_start, end_width=self.w_end)

        elems += Wedge(layer=WGclad, begin_coord=(0.0, 0.0), end_coord=(self.taperlen, 0.0),
                       begin_width=self.w_start+2.0*self.w_trench, end_width=self.w_end+2.0*self.w_trench)

        return elems




    def define_ports(self, ports):
        ports += OpticalPort(name="in", position=(0.0, 0.0), angle=180,
                             wg_definition=WgElDefinition(wg_width=self.w_start,
                                                          trench_width=self.w_trench))
        ports += OpticalPort(name="out", position=(self.taperlen,0.0), angle=0,
                             wg_definition=WgElDefinition(wg_width=self.w_end,
                                                          trench_width=self.w_trench))
        return ports


class SplitterTree(Structure):
    __name_prefix__ = 'SplitterTree'


    xn = ListProperty(default=np.arange(0, 64.0*10.0, 10.0).tolist())
    x_sep = PositiveNumberProperty(default=80.0)
    bend_radius = PositiveNumberProperty(default=20.0)
    # print xn


    M1_width = PositiveNumberProperty(default=0.6)
    M2_width = PositiveNumberProperty(default=0.9)
    FCW_width = PositiveNumberProperty(default=0.5)
    M1Layer = PPLayer(process=TECH.PROCESS.M1, purpose=TECH.PURPOSE.LF.ISLAND)
    M2Layer = PPLayer(process=TECH.PROCESS.M2, purpose=TECH.PURPOSE.LF.ISLAND)
    FCWLayer = PPLayer(process=TECH.PROCESS.FCW, purpose=TECH.PURPOSE.DF.TRENCH)




    def define_elements(self,elems):
        # print len(self.xn)

        N = int(np.log10(len(self.xn))/np.log10(2.0))
        # print N

        # N = int(N)+1
        # print N

        position = []

        for i in range(N):

            p = np.zeros(2 ** i)

            for m in range(2 ** i):
                # print m
                x_start = int(0 + m * 2 ** (N - i))
                x_stop = int(2 ** (N - i) - 1 + m * 2 ** (N - i))

                # print "start"
                # print x_start
                # print "stop"
                # print x_stop

                p[int(m)] = np.sum(self.xn[x_start:x_stop + 1]) / (2 ** (N - i))
            position.append(p)
        position.append(self.xn)
        # print position

        # print range(N)
        for i in range(N):

            for m in range(2 ** i):
                out_1 = position[i + 1][1 + (2 ** i - 1)]
                out_2 = position[i + 1][0 + (2 ** i - 1)]
                elems += SRef(MMI1x2(out_sep=abs(out_1-out_2), bend_radius=self.bend_radius),
                              position=(self.x_sep*i, position[i][m]))
                x_span = MMI1x2(out_sep=abs(out_1-out_2), bend_radius=self.bend_radius).size_info().width
                elems += SRef(WireTaper(taperlen=self.x_sep-x_span), position=(self.x_sep * i+x_span, position[i][m]+(out_1-out_2)/2.0))
                elems += SRef(WireTaper(taperlen=self.x_sep-x_span), position=(self.x_sep * i+x_span, position[i][m]-(out_1-out_2)/2.0))

                if (out_1-out_2) <= 4.0:
                    center = (self.x_sep * i+x_span + (self.x_sep-x_span)/2.0, position[i][m])
                    length = self.x_sep-x_span
                    elems += Rectangle(layer=self.M1Layer,
                                       center=center,
                                       box_size=(length, self.M1_width))
                    elems += Rectangle(layer=self.M2Layer,
                                       center=center,
                                       box_size=(length, self.M2_width))
                    elems += Rectangle(layer=self.FCWLayer,
                                       center=center,
                                       box_size=(length, self.FCW_width))

        return elems


class MZI(Structure):
    __name_prefix__ = 'MZI'

    gap = PositiveNumberProperty(default=50.0)
    L_straight = PositiveNumberProperty(default=300.0)
    bend_radius = PositiveNumberProperty(default=20.0)


    def define_elements(self,elems):

        MMI = SRef(MMI1x2(out_sep=self.gap, bend_radius=self.bend_radius),
                   position=(0.0, 0.0))
        elems += MMI
        elems += MMI.transform_copy(HMirror(mirror_plane_x=0.0)+Translation((MMI.size_info().width*2.0+self.L_straight, 0.0)))
        elems += SRef(WireTaper(taperlen=self.L_straight),position=(MMI.size_info().width, self.gap/2.0))
        elems += SRef(WireTaper(taperlen=self.L_straight), position=(MMI.size_info().width, -self.gap / 2.0))


        return elems


class SplitterTreeTest(Structure):
    __name_prefix__ = 'SplitterTree_test'

    N_stage = IntProperty(default=4)
    gap = PositiveNumberProperty(default=60.0)
    xn = ListProperty(default=[112.5, 105, 90, 60])
    yn = ListProperty(default=[153.75, 97.5, 45, 0])
    x_sep = PositiveNumberProperty(default=80.0)
    bend_radius = PositiveNumberProperty(default=20.0)

    def define_elements(self,elems):



        for i in range(self.N_stage):
            # xn = np.sum((i + 1) * 2 ** i)
            # yn = np.sum((i + 1) * 2 ** i)
            out_1 = -self.xn[i]/2.0
            out_2 = self.xn[i]/2.0
            splitter = SRef(MMI1x2(out_sep=abs(out_1-out_2), bend_radius=self.bend_radius),
                          position=(self.x_sep*i, self.yn[i]))
            elems += splitter
            # x_span = MMI1x2(out_sep=abs(out_1-out_2), bend_radius=self.bend_radius).size_info().width
            elems += SRef(WireTaper(taperlen=self.x_sep-splitter.size_info().width), position=(i*self.x_sep-(self.x_sep-splitter.size_info().width), self.yn[i]))
            elems += SRef(WireTaper(taperlen=self.x_sep*(self.N_stage-i) - splitter.size_info().width),position=(splitter.size_info().width+self.x_sep*i, self.yn[i]+self.xn[i]/2.0))
            # elems += SRef(WireTaper(taperlen=self.x_sep-x_span), position=(self.x_sep * i+x_span, position[i][m]-(out_1-out_2)/2.0))
        elems += SRef(WireTaper(taperlen=self.x_sep * (self.N_stage - i) - splitter.size_info().width),
                      position=(splitter.size_info().width + self.x_sep * i, self.yn[i] - self.xn[i] / 2.0))

        return elems


class SiHeaterBox(Structure):
    __name_prefix__ = 'SiHeaterBox'
    L_Box = PositiveNumberProperty(default=204.3)
    W_Box = PositiveNumberProperty(default=8.05)

    # layers
    BoxLayer = PPLayer(process=TECH.PROCESS.GW1, purpose=TECH.PURPOSE.LF.LINE)


    def define_elements(self,elems):
        elems += Rectangle(layer=self.BoxLayer, center=(self.L_Box/2.0, 0.0),
                           box_size=(self.L_Box, self.W_Box))
        return elems


class InputRing(Structure):
    __name_prefix__ = 'InputRing'
    bend_radius1 = PositiveNumberProperty(default=7.0)
    gap1 = PositiveNumberProperty(default=0.15)
    L_dc1 = PositiveNumberProperty(default=6.2)
    w_port = PositiveNumberProperty(default=0.45)
    w_trench = PositiveNumberProperty(default=2.0)

    def define_elements(self, elems):
        wg_definition = WgElDefinition(wg_width=self.w_port, trench_width=self.w_trench)


        ring = RingRect180DropFilter(ring_wg_definition=wg_definition,
                                       coupler_wg_definitions=[wg_definition, wg_definition],
                                       coupler_spacings=[self.gap1+self.w_port, self.gap1+self.w_port],
                                       bend_radius=self.bend_radius1,
                                       straights=(self.L_dc1, 0.0))
        elems += SRef(ring, (0, 0))




        return elems


class MetalElDefinition(WindowWaveguideDefinition):
    wg_width = PositiveNumberProperty(default=1.0)
    width = PositiveNumberProperty(default=1.0)
    trench_width = NonNegativeIntProperty(default=0.0)
    process = ProcessProperty(default=TECH.PROCESS.M1)
    purpose = PurposeProperty(default=TECH.PURPOSE.DF_AREA)


    def define_windows(self):
        windows = []
        windows.append(PathWindow(layer=PPLayer(self.process, self.purpose),
                                  start_offset=-0.5 * self.width,
                                  end_offset=+0.5 * self.width))
        return windows


class RingHeaterMetal(Structure):
    __name_prefix__ = 'RingHeaterMetal'
    bend_radius = PositiveNumberProperty(default=10.0)
    MetalWidth = PositiveNumberProperty(default=0.6)
    w_trench = PositiveNumberProperty(default=2.0)
    gap = PositiveNumberProperty(default=8.2)
    L_straight = PositiveNumberProperty(default=8.0)
    L_dummy = PositiveNumberProperty(default=1.5)
    shift_dummy = PositiveNumberProperty(default=2.60)
    angle = PositiveNumberProperty(default=30.0)
    process = ProcessProperty(default=TECH.PROCESS.HM)
    purpose = PurposeProperty(default=TECH.PURPOSE.DF.TRENCH)



    def define_elements(self,elems):


        MetalWG_definition = MetalElDefinition(width=self.MetalWidth, process=self.process, purpose= self. purpose)
        bend1 = WgElBend(start_point=(np.sin(self.angle/180.0*np.pi)*self.bend_radius, (np.cos(self.angle/180.0*np.pi)-1)*self.bend_radius),
                         start_angle=-self.angle,
                         bend_radius=self.bend_radius,
                         wg_definition=MetalWG_definition,
                         angle=-180+self.angle*2.0)
        elems += bend1
        elems += bend1.transform_copy(HMirror(mirror_plane_x=0.0))

        #leftside

        heater_layer = PPLayer(process=self.process, purpose=self.purpose)

        gap_x = np.sin(self.angle/180.0*np.pi)*(self.bend_radius-self.MetalWidth/2.0)
        y_tip = (1-np.cos(self.angle/180.0*np.pi))*self.bend_radius + np.cos(self.angle/180.0*np.pi)*self.MetalWidth/2.0
        #up
        elems += Rectangle(layer=heater_layer, center=(-gap_x-self.MetalWidth/2.0, -y_tip+self.L_dummy/2.0),
                           box_size=(self.MetalWidth, self.L_dummy))

        elems += Rectangle(layer=heater_layer, center=(-gap_x-self.L_straight/2.0, -y_tip+self.L_dummy-self.MetalWidth/2.0),
                           box_size=(self.L_straight, self.MetalWidth))

        #down

        elems += Rectangle(layer=heater_layer, center=(-gap_x-self.MetalWidth/2.0, -2*self.bend_radius + y_tip - self.L_dummy/2.0),
                           box_size=(self.MetalWidth, self.L_dummy))

        elems += Rectangle(layer=heater_layer, center=(-gap_x-self.L_straight/2.0, -2*self.bend_radius + y_tip - self.L_dummy + self.MetalWidth/2.0),
                           box_size=(self.L_straight, self.MetalWidth))




        #rightside

        elems += Rectangle(layer=heater_layer,
                           center=(gap_x + self.MetalWidth / 2.0, -y_tip + self.L_dummy / 2.0),
                           box_size=(self.MetalWidth, self.L_dummy))

        elems += Rectangle(layer=heater_layer,
                           center=(gap_x + self.L_straight / 2.0, -y_tip + self.L_dummy - self.MetalWidth / 2.0),
                           box_size=(self.L_straight, self.MetalWidth))

        # down

        elems += Rectangle(layer=heater_layer,
                           center=(gap_x + self.MetalWidth / 2.0, -2 * self.bend_radius + y_tip - self.L_dummy / 2.0),
                           box_size=(self.MetalWidth, self.L_dummy))

        elems += Rectangle(layer=heater_layer, center=(
        gap_x + self.L_straight / 2.0, -2 * self.bend_radius + y_tip - self.L_dummy + self.MetalWidth / 2.0),
                           box_size=(self.L_straight, self.MetalWidth))

        return elems


class VernierRingMetalHeater(Structure):
    __name_prefix__ = 'VernierRing_MetalHeater'
    bend_radius1 = PositiveNumberProperty(default=10.3)
    bend_radius2 = PositiveNumberProperty(default=10.0)
    # bend_radius3 = PositiveNumberProperty(default=5.0)
    gap1 = PositiveNumberProperty(default=0.23)
    gap2 = PositiveNumberProperty(default=0.23)
    L_dc1 = NumberProperty(default=0.0)
    L_dc2 = NumberProperty(default=0.0)
    w_port = PositiveNumberProperty(default=0.45)
    w_trench = PositiveNumberProperty(default=2.0)
    x_shift = PositiveNumberProperty(default=30.0)

    def define_elements(self, elems):
        wg_definition = WgElDefinition(wg_width=self.w_port, trench_width=self.w_trench)
        ring1 = RingRectNotchFilter(ring_wg_definition=wg_definition,
                                     coupler_wg_definitions=[wg_definition],
                                     coupler_spacings=[self.gap1+self.w_port],
                                     bend_radius=self.bend_radius1,
                                     straights=(
                                     self.L_dc1, 0.0))  # setting one or two straights to 0 will make a racetract or circle
        elems += SRef(ring1, (ring1.size_info().width/2.0, self.bend_radius1+self.w_port+self.gap1))

        ring2 = RingRect180DropFilter(ring_wg_definition=wg_definition,
                                       coupler_wg_definitions=[wg_definition, wg_definition],
                                       coupler_spacings=[self.gap2+self.w_port, self.gap2+self.w_port],
                                       bend_radius=self.bend_radius2,
                                       straights=(self.L_dc2, 0.0))
        elems += SRef(ring2, (ring2.size_info().width/2.0+self.x_shift, self.bend_radius2+self.w_port*3.0+self.gap2+self.bend_radius1*2+self.gap1*2))

        elems += SRef(WireTaper(taperlen=self.x_shift),
                      position=(0.0, 0.0+self.gap1*2.0+self.w_port*2.0+self.bend_radius1*2.0))

        elems += SRef(RingHeaterMetal(bend_radius=self.bend_radius1, gap=8.3, shift_dummy=1.75),
                      position=(ring1.size_info().width/2.0, 0.0+self.gap1+self.w_port+self.bend_radius1*2.0))

        elems += SRef(RingHeaterMetal(bend_radius=self.bend_radius2, gap=7.9, shift_dummy=1.85),
                      position=(ring2.size_info().width/2.0+self.x_shift,
                                self.bend_radius2*2.0+self.w_port*3.0+self.gap2+self.bend_radius1*2+self.gap1*2))
        return elems


class RingHeaterSi(Structure):
    __name_prefix__ = 'RingHeaterSi'
    bend_radius = PositiveNumberProperty(default=10.0)
    # w_port = PositiveNumberProperty(default=0.45)
    MetalWidth = PositiveNumberProperty(default=1.2)
    w_trench = PositiveNumberProperty(default=2.0)
    gap = PositiveNumberProperty(default=8.2)
    L_straight = PositiveNumberProperty(default=6.0)
    L_dummy = PositiveNumberProperty(default=1.0)
    shift_dummy = PositiveNumberProperty(default=1.85)
    angle = PositiveNumberProperty(default=45.0)
    process = ProcessProperty(default=TECH.PROCESS.N1)
    purpose = PurposeProperty(default=TECH.PURPOSE.DF_AREA)
    ext_in = BoolProperty(default = False)


    def define_elements(self,elems):

        heater_layer = PPLayer(process=self.process, purpose=self.purpose)

        radius1 = self.bend_radius

        MetalWG_definition = MetalElDefinition(wg_width=self.MetalWidth, process = self.process, purpose = self.purpose)
        bend1 = WgElBend(start_point=(np.sin(self.angle/180.0*np.pi)*radius1, (np.cos(self.angle/180.0*np.pi)-1)*radius1),
                         start_angle=-self.angle,
                         bend_radius=radius1,
                         wg_definition=MetalWG_definition,
                         angle=-180+self.angle*2.0)
        elems += bend1
        elems += bend1.transform_copy(HMirror(mirror_plane_x=0.0))


        if self.ext_in:
            gap = np.sin(self.angle / 180.0 * np.pi) * (radius1 + self.MetalWidth / 2.0) * 2.0
            elems += Rectangle(layer=heater_layer, center=(-gap / 2.0 + self.L_straight / 2.0, (np.cos(self.angle / 180.0 * np.pi) - 1) * (radius1+self.MetalWidth/2.0)),
                               box_size=(self.L_straight, self.MetalWidth))

            elems += Rectangle(layer=heater_layer, center=(-gap / 2.0 + self.L_straight / 2.0,
                                                           -bend1.size_info().height + (np.cos(
                                                               self.angle / 180.0 * np.pi) - 1) * (radius1-self.MetalWidth/2.0) + self.MetalWidth * np.cos(
                                                               self.angle / 180.0 * np.pi)),
                               box_size=(self.L_straight, self.MetalWidth))

            elems += Rectangle(layer=heater_layer, center=(gap/2.0-self.L_straight/2.0, (np.cos(self.angle/180.0*np.pi)-1)*(radius1+self.MetalWidth/2.0)),
                               box_size=(self.L_straight, self.MetalWidth))

            elems += Rectangle(layer=heater_layer, center=(gap/2.0-self.L_straight/2.0, -bend1.size_info().height+(np.cos(self.angle/180.0*np.pi)-1)*(radius1-self.MetalWidth/2.0)+self.MetalWidth*np.cos(self.angle/180.0*np.pi)),
                               box_size=(self.L_straight, self.MetalWidth))

        else:
        #leftside

            gap = np.sin(self.angle / 180.0 * np.pi) * (radius1 - self.MetalWidth / 2.0) * 2.0
            elems += Rectangle(layer=heater_layer, center=(-gap/2.0-self.L_straight/2.0, (np.cos(self.angle/180.0*np.pi)-1)*(radius1+self.MetalWidth/2.0)),
                               box_size=(self.L_straight, self.MetalWidth))

            elems += Rectangle(layer=heater_layer, center=(-gap/2.0-self.L_straight/2.0, -bend1.size_info().height+(np.cos(self.angle/180.0*np.pi)-1)*(radius1-self.MetalWidth/2.0)+self.MetalWidth*np.cos(self.angle/180.0*np.pi)),
                               box_size=(self.L_straight, self.MetalWidth))

            elems += Rectangle(layer=heater_layer, center=(-gap/2.0-self.shift_dummy, (np.cos(self.angle/180.0*np.pi)-1)*(radius1+self.MetalWidth/2.0)-self.MetalWidth*1.0/2.0),
                               box_size=(self.L_dummy, self.MetalWidth*2.0))

            elems += Rectangle(layer=heater_layer, center=(-gap/2.0-self.shift_dummy, -bend1.size_info().height+(np.cos(self.angle/180.0*np.pi)-1)*(radius1-self.MetalWidth/2.0)+self.MetalWidth*np.cos(self.angle/180.0*np.pi)+self.MetalWidth*1.0/2.0),
                               box_size=(self.L_dummy, self.MetalWidth*2.0))

            #rightside

            elems += Rectangle(layer=heater_layer, center=(gap/2.0+self.L_straight/2.0, (np.cos(self.angle/180.0*np.pi)-1)*(radius1+self.MetalWidth/2.0)),
                               box_size=(self.L_straight, self.MetalWidth))

            elems += Rectangle(layer=heater_layer, center=(gap/2.0+self.L_straight/2.0, -bend1.size_info().height+(np.cos(self.angle/180.0*np.pi)-1)*(radius1-self.MetalWidth/2.0)+self.MetalWidth*np.cos(self.angle/180.0*np.pi)),
                               box_size=(self.L_straight, self.MetalWidth))

            elems += Rectangle(layer=heater_layer, center=(gap / 2.0 + self.shift_dummy, (
                        np.cos(self.angle / 180.0 * np.pi) - 1) * (radius1+self.MetalWidth/2.0) - self.MetalWidth * 1.0 / 2.0),
                               box_size=(self.L_dummy, self.MetalWidth * 2.0))

            elems += Rectangle(layer=heater_layer, center=(gap / 2.0 + self.shift_dummy,
                                                                -bend1.size_info().height + (np.cos(self.angle / 180.0 * np.pi) - 1) * (radius1-self.MetalWidth/2.0) + self.MetalWidth * np.cos(
                                                                self.angle / 180.0 * np.pi) + self.MetalWidth * 1.0 / 2.0),
                               box_size=(self.L_dummy, self.MetalWidth * 2.0))



        return elems


class VernierRingSiHeater(Structure):
    __name_prefix__ = 'VernierRingSiHeater'
    bend_radius1 = PositiveNumberProperty(default=10.3)
    bend_radius2 = PositiveNumberProperty(default=10.0)
    gap1 = PositiveNumberProperty(default=0.23)
    gap2 = PositiveNumberProperty(default=0.23)
    L_dc1 = NumberProperty(default=0.0)
    L_dc2 = NumberProperty(default=0.0)
    w_port = PositiveNumberProperty(default=0.45)
    w_trench = PositiveNumberProperty(default=2.0)
    x_shift = PositiveNumberProperty(default=30.0)

    WGclad = PPLayer(process=TECH.PROCESS.WG, purpose=TECH.PURPOSE.LF_AREA)

    def define_elements(self, elems):
        wg_definition = WgElDefinition(wg_width=self.w_port, trench_width=self.w_trench)
        ring1 = RingRectNotchFilter(ring_wg_definition=wg_definition,
                                     coupler_wg_definitions=[wg_definition],
                                     coupler_spacings=[self.gap1+self.w_port],
                                     bend_radius=self.bend_radius1,
                                     straights=(
                                     self.L_dc1, 0.0))  # setting one or two straights to 0 will make a racetract or circle
        elems += SRef(ring1, (ring1.size_info().width/2.0, self.bend_radius1+self.w_port+self.gap1))

        ring2 = RingRect180DropFilter(ring_wg_definition=wg_definition,
                                       coupler_wg_definitions=[wg_definition, wg_definition],
                                       coupler_spacings=[self.gap2+self.w_port, self.gap2+self.w_port],
                                       bend_radius=self.bend_radius2,
                                       straights=(self.L_dc2, 0.0))
        elems += SRef(ring2, (ring2.size_info().width/2.0+self.x_shift, self.bend_radius2+self.w_port*3.0+self.gap2+self.bend_radius1*2+self.gap1*2))

        elems += SRef(WireTaper(taperlen=self.x_shift),
                      position=(0.0, 0.0+self.gap1*2.0+self.w_port*2.0+self.bend_radius1*2.0))

        radius11 = self.bend_radius1 + 1.425
        radius12 = self.bend_radius1 - 1.425
        radius21 = self.bend_radius2 + 1.425
        radius22 = self.bend_radius2 - 1.425
        process = [TECH.PROCESS.WG, TECH.PROCESS.N1, TECH.PROCESS.NPLUS]
        purpose = [TECH.PURPOSE.LF.LINE, TECH.PURPOSE.DF_AREA, TECH.PURPOSE.DF_AREA]
        LW = [1.2, 1.0, 1.0]
        L_straight = [[6.0,4.0],[6.0-0.071,4.0-0.071],[6.0-0.071,4.0-0.071]]
        shift_dummy = [1.85, 1.80, 1.80]
        L_dummy = [1.00, 0.80, 0.80]
        for i in range(len(process)):
            # ring 1

            elems += SRef(RingHeaterSi(MetalWidth = LW[i], bend_radius=radius11, L_dummy=L_dummy[i],
                                       shift_dummy=shift_dummy[i], angle= 45, L_straight = L_straight[i][0],
                                       process = process[i], purpose = purpose[i]),
                          position=(ring1.size_info().width/2.0, 0.0+self.gap1+self.w_port+self.bend_radius1+radius11))

            elems += SRef(RingHeaterSi(MetalWidth = LW[i], bend_radius=radius12, L_dummy=L_dummy[i],
                                       shift_dummy=shift_dummy[i], angle= 45, ext_in = True, L_straight = L_straight[i][1],
                                       process = process[i], purpose = purpose[i]),
                          position=(ring1.size_info().width/2.0, 0.0+self.gap1+self.w_port+self.bend_radius1+radius12))

            if process[i] == TECH.PROCESS.WG:

                height_clad = SRef(RingHeaterSi(MetalWidth = LW[i], bend_radius=radius11, L_dummy=L_dummy[i], shift_dummy=2.00, angle= 45, L_straight = L_straight[i][0], process = process[i]),
                          position=(ring1.size_info().width/2.0, 0.0+self.gap1+self.w_port+self.bend_radius1+radius11)).size_info().height + 2*self.w_trench

                width_clad = SRef(RingHeaterSi(MetalWidth = LW[i], bend_radius=radius11, L_dummy=L_dummy[i], shift_dummy=2.00, angle= 45, L_straight = L_straight[i][0], process = process[i]),
                          position=(ring1.size_info().width/2.0, 0.0+self.gap1+self.w_port+self.bend_radius1+radius11)).size_info().width

                elems += Rectangle(layer=self.WGclad,center=(ring1.size_info().width/2.0-0.0005, 0.0+self.gap1+self.w_port+self.bend_radius1),
                                   box_size=(width_clad+0.001,height_clad))


            # ring 2

            elems += SRef(RingHeaterSi(MetalWidth = LW[i], bend_radius=radius21, L_dummy=L_dummy[i],
                                       shift_dummy=shift_dummy[i], angle= 45, L_straight = L_straight[i][0],
                                       process = process[i], purpose = purpose[i]),
                          position=(ring2.size_info().width/2.0+self.x_shift,
                                    self.bend_radius2*2.0+self.w_port*4.0+self.gap2*2.0+self.gap1*2+self.bend_radius2+radius21))

            elems += SRef(RingHeaterSi(MetalWidth = LW[i], bend_radius=radius22, L_dummy=L_dummy[i],
                                       shift_dummy=shift_dummy[i], angle= 45, ext_in = True, L_straight = L_straight[i][1],
                                       process = process[i], purpose = purpose[i]),
                          position=(ring2.size_info().width/2.0+self.x_shift,
                                    self.bend_radius2*2.0+self.w_port*4.0+self.gap2*2.0+self.gap1*2+self.bend_radius2+radius22))

            if process[i] == TECH.PROCESS.WG:

                height_clad = SRef(RingHeaterSi(MetalWidth = LW[i], bend_radius=radius21, L_dummy=L_dummy[i],
                                                shift_dummy=shift_dummy[i], angle= 45, L_straight = L_straight[i][0],
                                                process = process[i], purpose = purpose[i]),
                                    position=(ring1.size_info().width/2.0,
                                    0.0+self.gap1+self.w_port+self.bend_radius1+radius21)).size_info().height + 2*self.w_trench

                width_clad = 2.0* L_straight[i][0] + (radius21-LW[i]/2.0)*np.sin(45.0/180*np.pi)*2

                elems += Rectangle(layer=self.WGclad, center=(ring2.size_info().width/2.0+self.x_shift-0.0005,
                                                              self.bend_radius2*2.0+self.w_port*4.0+self.gap2*2.0+self.gap1*2+self.bend_radius2),
                                   box_size=(width_clad-0.001, height_clad))


        return elems


class RingHeaterPN(Structure):
    __name_prefix__ = 'RingHeaterPN'
    bend_radius = PositiveNumberProperty(default=10.0)
    # w_port = PositiveNumberProperty(default=0.45)
    MetalWidth = PositiveNumberProperty(default=0.5)
    w_trench = PositiveNumberProperty(default=2.0)
    gap = PositiveNumberProperty(default=8.2)
    L_straight = PositiveNumberProperty(default=6.0)
    L_dummy = PositiveNumberProperty(default=1.0)
    shift_dummy = PositiveNumberProperty(default=1.85)
    angle = ListProperty(default=[45.0, 45.0, 45.0, 45.0, 45.0, 44.0])
    process_outer = ListProperty(default=[TECH.PROCESS.PBODY,
                     TECH.PROCESS.PPLUS,
                     TECH.PROCESS.P1,
                     TECH.PROCESS.M1,
                     TECH.PROCESS.WG,
                     TECH.PROCESS.SAL])
    process_inner = ListProperty(default=[TECH.PROCESS.NBODY,
                     TECH.PROCESS.NPLUS,
                     TECH.PROCESS.N1,
                     TECH.PROCESS.M1,
                     TECH.PROCESS.WG,
                     TECH.PROCESS.SAL])
    purpose_outer = ListProperty(default=[TECH.PURPOSE.DF_AREA,
                     TECH.PURPOSE.DF_AREA,
                     TECH.PURPOSE.DF_AREA,
                     TECH.PURPOSE.LF.ISLAND,
                     TECH.PURPOSE.DF.TRENCH,
                     TECH.PURPOSE.DF_AREA])
    purpose_inner = ListProperty(default=[TECH.PURPOSE.DF_AREA,
                     TECH.PURPOSE.DF_AREA,
                     TECH.PURPOSE.DF_AREA,
                     TECH.PURPOSE.LF.ISLAND,
                     TECH.PURPOSE.DF.TRENCH,
                     TECH.PURPOSE.DF_AREA])
    dradius = ListProperty(default = [1.2625, 1.45, 1.0, 1.6625, 1.975, 1.4125])
    LW = ListProperty(default = [1.475, 0.9, 2.0, 1.4, 0.5, 0.625])
    cir_process = ProcessProperty(default=TECH.PROCESS.PCON)
    cir_purpose = PurposeProperty(default=TECH.PURPOSE.DF_AREA)


    def define_elements(self,elems):


        radius1 = np.asarray(self.dradius) + self.bend_radius
        radius2 = -np.asarray(self.dradius) + self.bend_radius

        for i in range(len(self.process_inner)):
            # ring 1

            if self.process_inner[i] == TECH.PROCESS.WG:

                angle = self.angle[i] - 7.0
                layer1_definition = MetalElDefinition(width=self.LW[i], process=self.process_outer[i], purpose=self.purpose_outer[i])
                bend1 = WgElBend(start_point=(np.sin(angle / 180.0 * np.pi) * radius1[i], np.cos(angle / 180.0 * np.pi) * radius1[i]),
                                 start_angle=-angle,
                                 bend_radius=radius1[i],
                                 wg_definition=layer1_definition,
                                 angle=-180 + angle * 2.0)
                layer2_definition = MetalElDefinition(width=self.LW[i], process=self.process_inner[i], purpose=self.purpose_inner[i])
                bend2 = WgElBend(start_point=(np.sin(angle / 180.0 * np.pi) * radius2[i], np.cos(angle / 180.0 * np.pi) * radius2[i]),
                                 start_angle=-angle,
                                 bend_radius=radius2[i],
                                 wg_definition=layer2_definition,
                                 angle=-180 + angle * 2.0)

                elems += bend1
                elems += bend1.transform_copy(HMirror(mirror_plane_x=0.0))
                elems += bend2
                elems += bend2.transform_copy(HMirror(mirror_plane_x=0.0))
                elems += bend2.transform_copy(Rotation(rotation_center=(0.0, 0.0), rotation=90.0))
                elems += bend2.transform_copy(HMirror(mirror_plane_x=0.0)+Rotation(rotation_center=(0.0, 0.0), rotation=90.0))

            else:
                angle = self.angle[i]
                layer1_definition = MetalElDefinition(width=self.LW[i], process=self.process_outer[i], purpose=self.purpose_outer[i])
                bend1 = WgElBend(start_point=(
                np.sin(angle / 180.0 * np.pi) * radius1[i], np.cos(angle / 180.0 * np.pi) * radius1[i]),
                                 start_angle=-angle,
                                 bend_radius=radius1[i],
                                 wg_definition=layer1_definition,
                                 angle=-180 + angle * 2.0)
                layer2_definition = MetalElDefinition(width=self.LW[i], process=self.process_inner[i], purpose=self.purpose_inner[i])
                bend2 = WgElBend(start_point=(
                np.sin(angle / 180.0 * np.pi) * radius2[i], np.cos(angle / 180.0 * np.pi) * radius2[i]),
                                 start_angle=-angle,
                                 bend_radius=radius2[i],
                                 wg_definition=layer2_definition,
                                 angle=-180 + angle * 2.0)

                elems += bend1
                elems += bend1.transform_copy(HMirror(mirror_plane_x=0.0))
                elems += bend2
                elems += bend2.transform_copy(HMirror(mirror_plane_x=0.0))

        cir_layer = PPLayer(process=self.cir_process, purpose=self.cir_purpose)
        # r = 0.123
        # Npts_cir = 25
        # Npts_cir_angle = np.linspace(0, 360, Npts_cir) / 180.0 * np.pi
        # pts_cir = []
        # for i in range(Npts_cir):
        #     pts_cir.append((r * np.sin(Npts_cir_angle[i]), r * np.cos(Npts_cir_angle[i])))

        pts_cir = [(-0.02000, - 0.12300), (-0.05700, - 0.11100), (-0.08800, - 0.08800), (-0.11100, - 0.05700),
                 (-0.12300, - 0.02000), (-0.12300, 0.02000), (-0.11100, 0.05700), (-0.08800, 0.08800),
                 (-0.05700, 0.11100), (-0.02000, 0.12300), (0.02000, 0.12300), (0.05700, 0.11100), (0.08800, 0.08800),
                 (0.11100, 0.05700), (0.12300, 0.02000), (0.12300, - 0.02000), (0.11100, - 0.05700),
                 (0.08800, - 0.08800), (0.05700, - 0.11100), (0.02000, - 0.12300)]

        dot = Boundary(layer=cir_layer, shape=Shape(points=pts_cir))

        N_cir_outer = 27
        N_cir_angle_outer = np.linspace(self.angle[5]+2.0, 180.0-self.angle[5]-2.0, N_cir_outer) / 180.0 * np.pi
        for i in range(N_cir_outer):

            elems += dot.transform_copy(
                Translation((np.sin(N_cir_angle_outer[i]) * radius1[5], np.cos(N_cir_angle_outer[i]) * radius1[5])))

            elems += dot.transform_copy(
                Translation((-np.sin(N_cir_angle_outer[i]) * radius1[5], np.cos(N_cir_angle_outer[i]) * radius1[5])))

        N_cir_inner = 20
        N_cir_angle_inner = np.linspace(self.angle[5] + 2.0, 180.0 - self.angle[5] - 2.0, N_cir_inner) / 180.0 * np.pi
        for i in range(N_cir_inner):

            elems += dot.transform_copy(
                Translation((np.sin(N_cir_angle_inner[i]) * radius2[5], np.cos(N_cir_angle_inner[i]) * radius2[5])))

            elems += dot.transform_copy(
                Translation((-np.sin(N_cir_angle_inner[i]) * radius2[5], np.cos(N_cir_angle_inner[i]) * radius2[5])))

        return elems


class VernierRingPNHeater(Structure):
    __name_prefix__ = 'VernierRingPNHeater'
    bend_radius1 = PositiveNumberProperty(default=10.3)
    bend_radius2 = PositiveNumberProperty(default=10.0)
    gap1 = PositiveNumberProperty(default=0.38)
    gap2 = PositiveNumberProperty(default=0.38)
    L_dc1 = NumberProperty(default=0.0)
    L_dc2 = NumberProperty(default=0.0)
    w_port = PositiveNumberProperty(default=0.45)
    w_trench = PositiveNumberProperty(default=0.775)
    x_shift = PositiveNumberProperty(default=30.0)
    angle = PositiveNumberProperty(default=45.0)
    WGclad = PPLayer(process=TECH.PROCESS.WG, purpose=TECH.PURPOSE.LF_AREA)

    def define_elements(self, elems):
        wg_definition = WgElDefinition(wg_width=self.w_port, trench_width=self.w_trench, process = TECH.PROCESS.SK)
        ring1 = RingRectNotchFilter(ring_wg_definition=wg_definition,
                                     coupler_wg_definitions=[wg_definition],
                                     coupler_spacings=[self.gap1+self.w_port],
                                     bend_radius=self.bend_radius1,
                                     straights=(
                                     self.L_dc1, 0.0))  # setting one or two straights to 0 will make a racetract or circle
        elems += SRef(ring1, (ring1.size_info().width/2.0, self.bend_radius1+self.w_port+self.gap1))

        ring2 = RingRect180DropFilter(ring_wg_definition=wg_definition,
                                       coupler_wg_definitions=[wg_definition, wg_definition],
                                       coupler_spacings=[self.gap2+self.w_port, self.gap2+self.w_port],
                                       bend_radius=self.bend_radius2,
                                       straights=(self.L_dc2, 0.0))
        elems += SRef(ring2, (ring2.size_info().width/2.0+self.x_shift, self.bend_radius2+self.w_port*3.0+self.gap2+self.bend_radius1*2+self.gap1*2))

        elems += SRef(WireTaper(taperlen=self.x_shift, w_trench=self.w_trench, process = TECH.PROCESS.SK),
                      position=(0.0, 0.0+self.gap1*2.0+self.w_port*2.0+self.bend_radius1*2.0))


        elems += SRef(Transition(), position=(ring1.size_info().width, 0.0))
        elems += SRef(Transition(), position=(0.0, 0.0)).transform_copy(HMirror(mirror_plane_x=0.0))

        elems += SRef(Transition(), position=(0.0, 0.0+self.gap1*2.0+self.w_port*2.0+self.bend_radius1*2.0)).transform_copy(HMirror(mirror_plane_x=0.0))
        elems += SRef(Transition(), position=(self.x_shift+ring2.size_info().width, 0.0+self.gap1*2.0+self.w_port*2.0+self.bend_radius1*2.0))

        y_shift = self.gap1*2.0+self.w_port*2.0+self.bend_radius1*2.0+self.gap2*2.0+self.w_port*2.0+self.bend_radius2*2.0
        elems += SRef(Transition(), position=(self.x_shift + ring2.size_info().width, y_shift))
        elems += SRef(Transition(), position=(self.x_shift, y_shift)).transform_copy(HMirror(mirror_plane_x=0.0))

        dradius = [1.2625, 1.45, 1.0, 1.6625, 2.2, 1.4125]

        LW = [1.475, 0.9, 2.0, 1.4, 0.6, 0.625]
        angle = [45.0, 45.0, 45.0, 45.0, 45.0, 47.0]
        process_outer = [TECH.PROCESS.PBODY,
                         TECH.PROCESS.PPLUS,
                         TECH.PROCESS.P1,
                         TECH.PROCESS.M1,
                         TECH.PROCESS.WG,
                         TECH.PROCESS.SAL]
        purpose_outer = [TECH.PURPOSE.DF_AREA,
                         TECH.PURPOSE.DF_AREA,
                         TECH.PURPOSE.DF_AREA,
                         TECH.PURPOSE.LF.ISLAND,
                         TECH.PURPOSE.DF.TRENCH,
                         TECH.PURPOSE.DF_AREA]

        process_inner = [TECH.PROCESS.PBODY,
                         TECH.PROCESS.PPLUS,
                         TECH.PROCESS.P1,
                         TECH.PROCESS.M1,
                         TECH.PROCESS.WG,
                         TECH.PROCESS.SAL]
        purpose_inner = [TECH.PURPOSE.DF_AREA,
                         TECH.PURPOSE.DF_AREA,
                         TECH.PURPOSE.DF_AREA,
                         TECH.PURPOSE.LF.ISLAND,
                         TECH.PURPOSE.DF.TRENCH,
                         TECH.PURPOSE.DF_AREA]

        cir_process = TECH.PROCESS.PCON
        cir_purpose = TECH.PURPOSE.DF_AREA

        elems += SRef(RingHeaterPN(LW=LW, bend_radius=self.bend_radius1, dradius=dradius, angle=angle,
                                   cir_process=cir_process, cir_purpose=cir_purpose,
                                   process_outer=process_outer, purpose_outer=purpose_outer,
                                   process_inner=process_inner, purpose_inner=purpose_inner),
                      position=(ring1.size_info().width/2.0, 0.0 + self.gap1 + self.w_port + 1.0*self.bend_radius1))

        elems += SRef(RingHeaterPN(LW=LW, bend_radius=self.bend_radius2, dradius=dradius, angle=angle,
                                   cir_process=cir_process, cir_purpose=cir_purpose,
                                   process_outer=process_outer, purpose_outer=purpose_outer,
                                   process_inner=process_inner, purpose_inner=purpose_inner),
                      position=(ring2.size_info().width / 2.0 + self.x_shift,
                                self.w_port * 3.0 + self.gap1 * 2.0 + self.bend_radius1 * 2.0 + self.gap2 * 1.0 + self.bend_radius2))


        SKclad = PPLayer(process=TECH.PROCESS.SK, purpose=TECH.PURPOSE.LF_AREA)
        x = [5.8, 6.4, 5.6, 6.3]
        y = -self.w_trench-self.w_port/2.0 + self.gap1 * 2.0 + self.w_port * 2.0 + self.bend_radius1 * 2.0
        yshift = [-20.16, 19.56]


        elems += Rectangle(layer=SKclad, center=((x[1]+x[0])/2.0, y), box_size=(x[1]-x[0], 1))
        elems += Rectangle(layer=SKclad, center=(ring1.size_info().width-(x[1] + x[0]) / 2.0, y), box_size=(x[1] - x[0], 1))
        elems += Rectangle(layer=SKclad, center=((x[1]+x[0])/2.0, y + yshift[0]), box_size=(x[1]-x[0], 1))
        elems += Rectangle(layer=SKclad, center=(ring1.size_info().width-(x[1] + x[0]) / 2.0, y + yshift[0]), box_size=(x[1] - x[0], 1))

        elems += Rectangle(layer=SKclad, center=(self.x_shift+ring2.size_info().width-(x[2]+x[3])/2.0, y+self.w_port+self.w_trench*2.0), box_size=(x[3]-x[2], 1))
        elems += Rectangle(layer=SKclad, center=(self.x_shift + (x[2] + x[3]) / 2.0, y + self.w_port + self.w_trench * 2.0),box_size=(x[3] - x[2], 1))
        elems += Rectangle(layer=SKclad, center=(self.x_shift+ring2.size_info().width-(x[2]+x[3])/2.0, yshift[1] + y+self.w_port+self.w_trench*2.0), box_size=(x[3]-x[2], 1))
        elems += Rectangle(layer=SKclad, center=(self.x_shift + (x[2] + x[3]) / 2.0, yshift[1] + y + self.w_port + self.w_trench * 2.0),box_size=(x[3] - x[2], 1))




        return elems


class DC(Structure):
    __name_prefix__ = 'DC'
    bend_radius = PositiveNumberProperty(default=7.0)
    gap = PositiveNumberProperty(default=0.15)
    straight = PositiveNumberProperty(default=14.17)
    shift = PositiveNumberProperty(default=10.0)
    w_port = PositiveNumberProperty(default=0.45)
    w_trench = PositiveNumberProperty(default=2.0)

    # layers
    WGcore = PPLayer(process=TECH.PROCESS.WG, purpose=TECH.PURPOSE.LF.LINE)
    WGclad = PPLayer(process=TECH.PROCESS.WG, purpose=TECH.PURPOSE.LF_AREA)


    def define_elements(self,elems):

        wg_definition = WgElDefinition(wg_width=self.w_port, trench_width=self.w_trench)


        # bend
        port1 = OpticalPort(position=(self.straight/2.0, self.gap / 2.0+self.w_port/2.0), angle=0,
                            wg_definition=wg_definition)

        port2 = OpticalPort(position=(self.straight/2.0, -self.gap / 2.0-self.w_port/2.0), angle=0,
                            wg_definition=wg_definition)



        bend1 = RouteConnectorRounded(
            RouteToEastAtY(input_port=port1, bend_radius=self.bend_radius, y_position=self.shift,
                           min_straight=0.0))
        bend2 = RouteConnectorRounded(
            RouteToEastAtY(input_port=port2, bend_radius=self.bend_radius, y_position=-self.shift,
                           min_straight=0.0))
        elems += bend1
        elems += bend2
        elems += SRef(WireTaper(taperlen=self.straight), position=(-self.straight/2.0, self.gap / 2.0+self.w_port/2.0))
        elems += SRef(WireTaper(taperlen=self.straight),
                      position=(-self.straight / 2.0, -self.gap / 2.0 - self.w_port / 2.0))

        port3 = OpticalPort(
            position=(-self.straight / 2.0 - bend1.size_info().width, self.shift), angle=0,
            wg_definition=wg_definition)

        port4 = OpticalPort(position=(-self.straight / 2.0 - bend1.size_info().width, -self.shift), angle=0,
                            wg_definition=wg_definition)

        bend3 = RouteConnectorRounded(
            RouteToEastAtY(input_port=port3, bend_radius=self.bend_radius, y_position=self.gap / 2.0 + self.w_port / 2.0,
                           min_straight=0.0))
        bend4 = RouteConnectorRounded(
            RouteToEastAtY(input_port=port4, bend_radius=self.bend_radius, y_position=-self.gap / 2.0 - self.w_port / 2.0,
                           min_straight=0.0))

        elems += bend3
        elems += bend4

        elems += Rectangle(layer=self.WGclad, center=(self.straight/2.0+bend1.size_info().width/2.0, 0.0),
                           box_size=(bend1.size_info().width, self.shift*2.0+self.w_port+2.0*self.w_trench))
        elems += Rectangle(layer=self.WGclad, center=(-self.straight/2.0-bend3.size_info().width/2.0, 0.0),
                           box_size=(bend1.size_info().width, self.shift*2.0+self.w_port+2.0*self.w_trench))

        return elems


class PhaseShifterArrayEqual(Structure):
    __name_prefix__ = 'PhaseShifterArrayEqual'

    xn_start = ListProperty(default=np.arange(0, 128.0, 2.0).tolist())
    xn_stop = ListProperty(default=np.arange(0, 128.0, 2.0).tolist())
    Shift = PositiveNumberProperty(default=300)
    w_port = PositiveNumberProperty(default=0.45)
    w_trench = PositiveNumberProperty(default=2.0)
    gap_heater = PositiveNumberProperty(default=12.0)
    L_straight = PositiveNumberProperty(default=10.0)
    L_heater = PositiveNumberProperty(default=204.6)

    M1_width = PositiveNumberProperty(default=0.6)
    M2_width = PositiveNumberProperty(default=0.9)
    FCW_width = PositiveNumberProperty(default=0.5)
    M1Layer = PPLayer(process=TECH.PROCESS.M1, purpose=TECH.PURPOSE.LF.ISLAND)
    M2Layer = PPLayer(process=TECH.PROCESS.M2, purpose=TECH.PURPOSE.LF.ISLAND)
    FCWLayer = PPLayer(process=TECH.PROCESS.FCW, purpose=TECH.PURPOSE.DF.TRENCH)

    def define_elements(self, elems):

        tobe_connected = []
        N_channel = len(self.xn_start)
        for i in range(N_channel):
            ports_in = (OpticalPort(position=(0, self.xn_start[i]), angle=0,
                                   wg_definition=WgElDefinition(wg_width=self.w_port, trench_width=self.w_trench)))
            ports_H1 = (OpticalPort(position=(self.L_straight+self.gap_heater*i, -self.L_straight), angle=90,
                                   wg_definition=WgElDefinition(wg_width=self.w_port, trench_width=self.w_trench)))
            tobe_connected += [[ports_in, ports_H1]]

        for i in range(N_channel):
            ports_H2 = (OpticalPort(position=(self.L_straight+self.gap_heater*i, -self.L_heater-self.L_straight), angle=-90,
                                   wg_definition=WgElDefinition(wg_width=self.w_port, trench_width=self.w_trench)))

            ports_out = (OpticalPort(position=((N_channel-1)*self.gap_heater+2.0*self.L_straight, -self.xn_stop[N_channel-i-1]-self.L_heater-2.0*self.L_straight), angle=180,
                                   wg_definition=WgElDefinition(wg_width=self.w_port, trench_width=self.w_trench)))

            tobe_connected += [[ports_H2, ports_out]]

        for ports in tobe_connected:
            manhattan_route = RouteManhattan(input_port=ports[0], output_port=ports[1])
            manhattan_connection = RouteConnectorManhattan(manhattan_route)
            elems += manhattan_connection

        for i in range(N_channel-1):

            center1 = ((self.L_straight+self.gap_heater*i)/2.0, (self.xn_start[i]+self.xn_start[i+1])/2.0)
            center2 = ((self.L_straight+self.gap_heater*(i+1) + (N_channel-1)*self.gap_heater+2.0*self.L_straight)/2.0,
                       (-self.xn_stop[N_channel-i-1] - self.xn_stop[N_channel-i-2])/2.0 -self.L_heater-2.0*self.L_straight)

            center3 = (self.L_straight+self.gap_heater*(2*i+1)/2.0,
                       (((self.xn_start[i]+self.xn_start[i+1])/2.0)+(-self.xn_stop[N_channel-i-1] - self.xn_stop[N_channel-i-2])/2.0 -self.L_heater-2.0*self.L_straight)/2.0)

            length1 = self.L_straight+self.gap_heater*i
            length2 = ((N_channel - i - 2)*self.gap_heater + self.L_straight)
            length3 = -10.0+abs(-((self.xn_start[i]+self.xn_start[i+1])/2.0)+(-self.xn_stop[N_channel-i-1] - self.xn_stop[N_channel-i-2])/2.0 -self.L_heater-2.0*self.L_straight)


            elems += Rectangle(layer=self.FCWLayer,
                               center=center1,
                               box_size=(length1, self.FCW_width))



            elems += Rectangle(layer=self.FCWLayer,
                               center=center2,
                               box_size=(length2, self.FCW_width))


            centerM1M2 = (self.L_straight+self.gap_heater*(2*i+1)/2.0,-self.L_straight-self.L_heater/2.0)
            lengthM1M2 = self.L_heater

            elems += Rectangle(layer=self.M1Layer,
                               center=centerM1M2,
                               box_size=(self.M1_width*2.0,lengthM1M2-6.0))
            elems += Rectangle(layer=self.M2Layer,
                               center=centerM1M2,
                               box_size=(self.M2_width*2.0,lengthM1M2-6.0))
            elems += Rectangle(layer=self.FCWLayer,
                               center=center3,
                               box_size=(self.FCW_width*2.0,length3))




        return elems


class SbendConnectionFill(Structure):
    __name_prefix__ = 'SbendConnectionFill'
    bend_radius = PositiveNumberProperty(default=20.0)
    in_coor = ListProperty(default=[0.0, 0.0])
    out_coor = ListProperty(default=[20.0, 4.0])
    w_port = PositiveNumberProperty(default=0.45)
    w_trench = PositiveNumberProperty(default=2.0)
    bend_length = DefinitionProperty()
    process = ProcessProperty(default=TECH.PROCESS.N1)
    purpose = PurposeProperty(default=TECH.PURPOSE.DF_AREA)

    def define_elements(self, elems):


        wg_definition = MetalElDefinition(width=self.w_port, process=self.process, purpose=self.purpose)


        # bend
        port1 = OpticalPort(position=(self.in_coor[0], self.in_coor[1]), angle=0,
                            wg_definition=wg_definition)

        if self.out_coor[1]-self.in_coor[1] == 0:
            elems += Rectangle(layer = PPLayer(process=self.process, purpose=self.purpose),
                               center=(self.in_coor[0]+abs(self.out_coor[0] - self.in_coor[0])/2.0,self.out_coor[1]),
                               box_size=(abs(self.out_coor[0] - self.in_coor[0]),self.w_port))
        else:
            bend = RouteConnectorRounded(
                RouteToEastAtY(input_port=port1, bend_radius=self.bend_radius, y_position=self.out_coor[1],
                               min_straight=0.0))

            elems += bend


            if abs(self.out_coor[0]-self.in_coor[0])-bend.size_info().width <=0:
                print "error, increasing SbendConnection length"
            else:
                elems += Rectangle(layer=PPLayer(process=self.process, purpose=self.purpose),
                    center=(self.in_coor[0]+bend.size_info().width + ((self.out_coor[0]-self.in_coor[0])-bend.size_info().width) / 2.0, self.out_coor[1]),
                    box_size=((self.out_coor[0]-self.in_coor[0])-bend.size_info().width, self.w_port))

        return elems

    def define_bend_length(self):
        wg_definition = MetalElDefinition(width=self.w_port, process=self.process, purpose=self.purpose)
        port1 = OpticalPort(position=(self.in_coor[0], self.in_coor[1]), angle=0,
                            wg_definition=wg_definition)

        if self.out_coor[1]-self.in_coor[1] == 0:
            Lbend = 0.0
        else:
            bend = RouteConnectorRounded(
                RouteToEastAtY(input_port=port1, bend_radius=self.bend_radius, y_position=self.out_coor[1],
                               min_straight=0.0))

            Lbend = bend.size_info().width



        return Lbend


class SbendConnection(Structure):
    __name_prefix__ = 'SbendConnection'
    bend_radius = PositiveNumberProperty(default=20.0)
    in_coor = ListProperty(default=[0.0, 0.0])
    out_coor = ListProperty(default=[20.0, 4.0])
    w_port = PositiveNumberProperty(default=0.45)
    w_trench = PositiveNumberProperty(default=2.0)
    bend_length = DefinitionProperty()

    def define_elements(self, elems):

        wg_definition = WgElDefinition(wg_width=self.w_port, trench_width=self.w_trench)


        # bend
        port1 = OpticalPort(position=(self.in_coor[0], self.in_coor[1]), angle=0,
                            wg_definition=wg_definition)

        if self.out_coor[1]-self.in_coor[1] == 0:
            elems += SRef(WireTaper(taperlen=(self.out_coor[0] - self.in_coor[0]), w_trench=self.w_trench),position=(self.in_coor[0], self.out_coor[1]))
        else:
            bend = RouteConnectorRounded(
                RouteToEastAtY(input_port=port1, bend_radius=self.bend_radius, y_position=self.out_coor[1],
                               min_straight=0.0))

            elems += bend


            if abs(self.out_coor[0]-self.in_coor[0])-bend.size_info().width <=0:
                print "error, increasing SbendConnection length"
            else:
                elems += SRef(WireTaper(taperlen=(self.out_coor[0]-self.in_coor[0])-bend.size_info().width, w_trench=self.w_trench), position=(self.in_coor[0]+bend.size_info().width, self.out_coor[1]))

        return elems

    def define_bend_length(self):
        wg_definition = WgElDefinition(wg_width=self.w_port, trench_width=self.w_trench)
        port1 = OpticalPort(position=(self.in_coor[0], self.in_coor[1]), angle=0,
                            wg_definition=wg_definition)

        if self.out_coor[1]-self.in_coor[1] == 0:
            Lbend = 0.0
        else:
            bend = RouteConnectorRounded(
                RouteToEastAtY(input_port=port1, bend_radius=self.bend_radius, y_position=self.out_coor[1],
                               min_straight=0.0))

            Lbend = bend.size_info().width



        return Lbend


class PhaseShifterArrayUnequal(Structure):
    __name_prefix__ = 'PhaseShifterArrayEqual'

    xn_start = ListProperty(default=np.arange(0, 64.0*10.0, 10.0).tolist())
    xn_stop = ListProperty(default=[0.0, 4.1, 27.4, 31.4, 38.8, 42.9, 61.3, 74.7, 91.4, 103.2, 114.5, 124.6, 139.1, 146.1, 165.9, 188.9, 196.6, 208.2, 217.3, 225.4, 231.7, 254.1, 273.2, 277.2, 281.2, 293.9, 315.4, 326.0, 330.6, 343.3, 347.8, 355.8, 378.7, 402.3, 425.7, 449.7, 463.3, 485.6, 493.8, 510.2, 517.8, 529.0, 543.0, 548.7, 572.5, 581.2, 602.4, 607.5, 616.7, 628.2, 635.7, 643.5, 657.6, 670.0, 676.6, 690.9, 696.7, 709.7, 724.7, 729.2, 740.1, 752.3, 759.0, 768.0])
    bend_radius1 = PositiveNumberProperty(default=200)
    bend_radius2 = PositiveNumberProperty(default=300)
    w_port = PositiveNumberProperty(default=0.45)
    w_trench = PositiveNumberProperty(default=2.0)
    gap_heater = PositiveNumberProperty(default=12.0)
    L1 = PositiveNumberProperty(default=230.0)
    L2 = PositiveNumberProperty(default=250.0)
    L_heater = PositiveNumberProperty(default=399.6)

    M1_width = PositiveNumberProperty(default=0.6*1.0)
    M2_width = PositiveNumberProperty(default=0.9*1.0)
    FCW_width = PositiveNumberProperty(default=0.5*1.0)
    M1Layer = PPLayer(process=TECH.PROCESS.M1, purpose=TECH.PURPOSE.LF.ISLAND)
    M2Layer = PPLayer(process=TECH.PROCESS.M2, purpose=TECH.PURPOSE.LF.ISLAND)
    FCWLayer = PPLayer(process=TECH.PROCESS.FCW, purpose=TECH.PURPOSE.DF.TRENCH)
    M1process = ProcessProperty(default=TECH.PROCESS.M1)
    M2process = ProcessProperty(default=TECH.PROCESS.M2)
    FCWprocess = ProcessProperty(default=TECH.PROCESS.FCW)
    M1purpose = PurposeProperty(default=TECH.PURPOSE.LF.ISLAND)
    M2purpose = PurposeProperty(default=TECH.PURPOSE.LF.ISLAND)
    FCWpurpose = PurposeProperty(default=TECH.PURPOSE.DF.TRENCH)



    def define_elements(self, elems):
        tobe_connected1 = []
        tobe_connected2 = []
        N_channel = len(self.xn_start)
        gap_list = []

        for i in range(N_channel-1):
            gap = self.xn_stop[i+1]-self.xn_stop[i]
            gap_list.append(gap)

        for i in range(N_channel):
            coors_in = [0,self.xn_start[i]-np.mean(self.xn_start)]
            coors_H1 = [self.L1, self.gap_heater*i-self.gap_heater*N_channel/2.0]
            tobe_connected1 += [[coors_in, coors_H1]]

        for i in range(N_channel):
            coors_H2 = [self.L1+self.L_heater, self.gap_heater*i-self.gap_heater*N_channel/2.0]
            coors_out = [self.L1+self.L_heater+self.L2, self.xn_stop[i] - np.mean(self.xn_stop)]
            tobe_connected2 += [[coors_H2, coors_out]]
        L_bend1 = []
        L_bend2 = []

        for coors_pair1 in tobe_connected1:
            elems += SRef(SbendConnection(in_coor=coors_pair1[0], out_coor=coors_pair1[1], w_port=self.w_port,
                                          w_trench=self.gap_heater/2.0, bend_radius=self.bend_radius1))
            L_bend1.append(SbendConnection(in_coor=coors_pair1[0], out_coor=coors_pair1[1], w_port=self.w_port,
                                       w_trench=self.w_trench, bend_radius=self.bend_radius1).bend_length)

        for coors_pair2 in tobe_connected2:
            elems += SRef(SbendConnection(in_coor=coors_pair2[0], out_coor=coors_pair2[1], w_port=self.w_port,
                                          w_trench=np.max(gap_list)/2.0, bend_radius=self.bend_radius2))
            L_bend2.append(SbendConnection(in_coor=coors_pair2[0], out_coor=coors_pair2[1], w_port=self.w_port,
                                       w_trench=self.w_trench, bend_radius=self.bend_radius2).bend_length)

        tobe_connected3 = []
        tobe_connected4 = []
        N_channel = len(self.xn_start)-1
        for i in range(N_channel):
            coors_in3 = [0,(self.xn_start[i]+self.xn_start[i+1])/2.0-np.mean(self.xn_start)]
            coors_H13 = [self.L1, self.gap_heater*i -self.gap_heater*N_channel/2.0]
            tobe_connected3 += [[coors_in3, coors_H13]]

        for i in range(N_channel):
            coors_H23 = [self.L1+self.L_heater, self.gap_heater*i-self.gap_heater*N_channel/2.0]
            coors_out3 = [self.L1+self.L_heater+self.L2, (self.xn_stop[i]+self.xn_stop[i+1])/2.0 - np.mean(self.xn_stop)]
            tobe_connected4 += [[coors_H23, coors_out3]]


        for coors_pair3 in tobe_connected3:
            elems += SRef(SbendConnectionFill(in_coor=coors_pair3[0], out_coor=coors_pair3[1], w_port=self.M1_width*3.0,
                                          process=self.M1process, purpose=self.M1purpose, bend_radius=self.bend_radius1))


            elems += SRef(SbendConnectionFill(in_coor=coors_pair3[0], out_coor=coors_pair3[1], w_port=self.M2_width*3.0,
                                          process=self.M2process, purpose=self.M2purpose, bend_radius=self.bend_radius1))

            elems += SRef(SbendConnectionFill(in_coor=coors_pair3[0], out_coor=coors_pair3[1], w_port=self.FCW_width*3.0,
                                          process=self.FCWprocess, purpose=self.FCWpurpose, bend_radius=self.bend_radius1))




        for coors_pair4 in tobe_connected4:
            elems += SRef(SbendConnectionFill(in_coor=coors_pair4[0], out_coor=coors_pair4[1], w_port=self.M1_width,
                                          process=self.M1process, purpose=self.M1purpose, bend_radius=self.bend_radius2))

            elems += SRef(SbendConnectionFill(in_coor=coors_pair4[0], out_coor=coors_pair4[1], w_port=self.M2_width,
                                          process=self.M2process, purpose=self.M2purpose, bend_radius=self.bend_radius2))

            elems += SRef(SbendConnectionFill(in_coor=coors_pair4[0], out_coor=coors_pair4[1], w_port=self.FCW_width,
                                          process=self.FCWprocess, purpose=self.FCWpurpose, bend_radius=self.bend_radius2))



            center = (coors_pair4[0][0]-self.L_heater/2.0, coors_pair4[0][1])
            length = self.L_heater
            elems += Rectangle(layer=self.M1Layer,
                               center=center,
                               box_size=(length, self.M1_width*3.0))
            elems += Rectangle(layer=self.M2Layer,
                               center=center,
                               box_size=(length, self.M2_width*3.0))
            elems += Rectangle(layer=self.FCWLayer,
                               center=center,
                               box_size=(length, self.FCW_width*3.0))




        return elems


class AntennaArrayUnequal(Structure):
    __name_prefix__ = 'AntennaArrayUnequal'


    xn_stop = ListProperty(default=[0.0, 4.1, 27.4, 31.4, 38.8, 42.9, 61.3, 74.7, 91.4, 103.2, 114.5, 124.6, 139.1, 146.1, 165.9, 188.9, 196.6, 208.2, 217.3, 225.4, 231.7, 254.1, 273.2, 277.2, 281.2, 293.9, 315.4, 326.0, 330.6, 343.3, 347.8, 355.8, 378.7, 402.3, 425.7, 449.7, 463.3, 485.6, 493.8, 510.2, 517.8, 529.0, 543.0, 548.7, 572.5, 581.2, 602.4, 607.5, 616.7, 628.2, 635.7, 643.5, 657.6, 670.0, 676.6, 690.9, 696.7, 709.7, 724.7, 729.2, 740.1, 752.3, 759.0, 768.0])
    antenna_1 = DefinitionProperty()
    antenna_2 = DefinitionProperty()

    L1 = PositiveNumberProperty(default=770.0)
    L2 = PositiveNumberProperty(default=1200.0)
    # L1 = PositiveNumberProperty(default=200.0)
    # L2 = PositiveNumberProperty(default=200.0)
    shift = PositiveNumberProperty(default=2000.0)
    w_port = PositiveNumberProperty(default=0.45)

    M1_width = PositiveNumberProperty(default=0.6)
    M2_width = PositiveNumberProperty(default=0.9)
    FCW_width = PositiveNumberProperty(default=0.5)
    M1Layer = PPLayer(process=TECH.PROCESS.M1, purpose=TECH.PURPOSE.LF.ISLAND)
    M2Layer = PPLayer(process=TECH.PROCESS.M2, purpose=TECH.PURPOSE.LF.ISLAND)
    FCWLayer = PPLayer(process=TECH.PROCESS.FCW, purpose=TECH.PURPOSE.DF.TRENCH)

    def define_antenna_1(self):
        antenna_1 = SRef(reference=SideEtchAntenna(L=self.L1))
        return antenna_1

    def define_antenna_2(self):
        antenna_2 = SRef(reference=SideEtchAntenna(L=self.L2))
        return antenna_2



    def define_elements(self, elems):
        N_channel = len(self.xn_stop)

        WGclad = PPLayer(process=TECH.PROCESS.WG, purpose=TECH.PURPOSE.LF_AREA)

        gap_list = []
        for i in range(N_channel-1):
            gap = self.xn_stop[i+1]-self.xn_stop[i]
            gap_list.append(gap)
            if gap>=4.6 and gap<=4.75:

                L1 = self.antenna_1.size_info().width
                L2 = self.antenna_2.size_info().width
                elems += Rectangle(layer=WGclad, center=(L1 / 2.0, (self.xn_stop[i]+self.xn_stop[i+1])/2.0),
                                   box_size=(L1, 2.0))

                elems += Rectangle(layer=WGclad, center=(self.shift+ L2 / 2.0, (self.xn_stop[i]+self.xn_stop[i+1])/2.0),
                                   box_size=(L2, 2.0))





        for i in range(N_channel):
            # print i
            elems += self.antenna_1.transform_copy(Translation((0.0, self.xn_stop[i])))
            elems += self.antenna_2.transform_copy(Translation((self.shift, self.xn_stop[i])))


        for i in range(N_channel-1):
            # print i
            if gap_list[i] >= 8.0:
                M1_width = gap_list[i]/2.0 - 4.0 +self.M1_width
                M2_width = gap_list[i]/2.0 - 4.0 +self.M2_width
                FCW_width = gap_list[i]/2.0 - 4.0 + self.FCW_width
            else:
                M1_width = self.M1_width
                M2_width = self.M2_width
                FCW_width = self.FCW_width

            shift_dummy = 3.0

            elems += Rectangle(layer=self.M1Layer,
                               center=(shift_dummy+self.L1/2.0, (self.xn_stop[i]+self.xn_stop[i+1])/2.0),
                               box_size=(self.L1, M1_width))
            elems += Rectangle(layer=self.M2Layer,
                               center=(shift_dummy+self.L1 / 2.0, (self.xn_stop[i] + self.xn_stop[i + 1]) / 2.0),
                               box_size=(self.L1, M2_width))
            elems += Rectangle(layer=self.FCWLayer,
                               center=(shift_dummy+self.L1 / 2.0, (self.xn_stop[i] + self.xn_stop[i + 1]) / 2.0),
                               box_size=(self.L1, FCW_width))

            elems += Rectangle(layer=self.M1Layer,
                               center=(shift_dummy+self.L2 / 2.0+self.shift, (self.xn_stop[i] + self.xn_stop[i + 1]) / 2.0),
                               box_size=(self.L2, M1_width))
            elems += Rectangle(layer=self.M2Layer,
                               center=(shift_dummy+self.L2 / 2.0+self.shift, (self.xn_stop[i] + self.xn_stop[i + 1]) / 2.0),
                               box_size=(self.L2, M2_width))
            elems += Rectangle(layer=self.FCWLayer,
                               center=(shift_dummy+self.L2 / 2.0+self.shift, (self.xn_stop[i] + self.xn_stop[i + 1]) / 2.0),
                               box_size=(self.L2, FCW_width))

        return elems


class SideEtchAntenna(Structure):
    __name_prefix__ = 'SideEtchAntenna'

    L_in = PositiveNumberProperty(default=5.0)
    p_out = PositiveNumberProperty(default=20)
    np_out = PositiveNumberProperty(default=10.0)
    w_port = PositiveNumberProperty(default=0.45)
    w_trench = PositiveNumberProperty(default=2.0)
    ww = PositiveNumberProperty(default=0.6)
    L = PositiveNumberProperty(default=770)
    N_end = IntProperty(default=5)
    end_period = PositiveNumberProperty(default=0.991)
    PlotandPrint = BoolProperty(default=False)


    # layers
    WGcore = PPLayer(process=TECH.PROCESS.WG, purpose=TECH.PURPOSE.LF.LINE)
    WGclad = PPLayer(process=TECH.PROCESS.WG, purpose=TECH.PURPOSE.LF_AREA)





    def define_elements(self, elems):
        

        def p_dw(x):
            a = -3.483e-07
            b = 0.001777
            c = -0.09118
            d = 634.9
            p = a*x**3+b*x**2+c*x+d
            return p

        def dw_beta(x):
            a = 3.85316958e-04
            b = 3.37928377e-02
            c = 1.06915966e+00
            d = 2.32527783e+01
            e = 2.97756371e+01
            f = 4.01443410e+02
            dw = a*x**4 + b*x**3 + c*x**2 + d*x + e*np.exp(x) + f
            return dw

        elems += SRef(WireTaper(w_start=self.w_port, w_end=self.ww, taperlen=self.L_in, w_trench=self.w_trench), position=(0.0, 0.0))
        elems += Rectangle(layer=self.WGclad,
                           center=(self.L_in/2.0, 0.0),
                           box_size=(self.L_in, self.ww+self.w_trench*2.0))


        p0 = 638
        beta0 = 10*np.log10(1000.0/(self.L*1000*1.0001-p0))
        dw0 = dw_beta(beta0)
        period_list = [p0]
        dw_list = [np.round(dw0, 3)]
        beta_list = [beta0]
        z_list = [p0/2.0]


        while np.sum(period_list) <= self.L*1000:
            z = np.sum(period_list)+period_list[-1]/2.0
            # print(z)
            beta = 10*np.log10(1000.0/(self.L*1000*1.0001-z))
            # if beta <= -40:
            #     beta = -40
            # elif beta >= -1:
            #     beta = -1


            dw = dw_beta(beta)
            if dw <= 10:
                dw = 10
            elif dw >= 450:
                dw = 450
            dw_list.append(np.round(dw,3))
            period_list.append(np.round(p_dw(dw),3))
            beta_list.append(beta)
            z_list.append(z)



        period_list = np.asarray(period_list)/1000.0
        dw_list = np.asarray(dw_list)/1000.0
        N = len(period_list)


        if self.PlotandPrint:
            print dw_list
            print period_list

            x = np.asarray(z_list)/1000.0/1000.0
            y1 = np.asarray(dw_list)*1000
            y2 = np.asarray(beta_list)
            y3 = np.asarray(period_list) * 1000
            import matplotlib.pyplot as plt
            fig1, ax1 = plt.subplots(1)
            lns1 = ax1.plot(x, y1, "r-", label='dw', lw=2)
            ax1.set_xlabel(r"z($\mu$m)", fontsize=15)
            ax1.set_ylabel("dw(nm)", fontsize=15)
            # ax1.legend()

            ax2 = ax1.twinx()
            lns2 = ax2.plot(x, y3, "g-", label='period', lw=2)
            ax2.set_ylabel("period(nm)", fontsize=15)
            lns = lns1+lns2
            labs = [l.get_label() for l in lns]
            ax1.legend(lns, labs, loc=0)
            # ax2.legend()

            fig2, ax3 = plt.subplots(1)
            ax3.plot(x, y2, "b-", label='emission rate(dB/$\mu$ m)', lw=2)
            ax3.set_xlabel(r"z($\mu$m)", fontsize=15)
            ax3.set_ylabel(r"emission rate(dB/$\mu m$)", fontsize=15)
            ax3.legend(loc=0)

            plt.show()

        x0=self.L_in
        pts_core = []
        pts_clad = []
        period_list = np.round(period_list,decimals=3)
        dw_list = np.round(dw_list,decimals=3)

        for i in range(N):
            pts_core.append((x0, self.ww/2.0))
            pts_core.append((x0 + period_list[i] / 2.0, self.ww / 2.0))
            pts_core.append((x0 + period_list[i] / 2.0, (self.ww - dw_list[i]) / 2.0))
            pts_core.append((x0 + period_list[i], (self.ww - dw_list[i]) / 2.0))
            x0 = x0 + period_list[i]

        x_end = x0
        elems += Rectangle(layer=self.WGclad,
                           center=(self.L_in + (x_end-self.L_in)/2.0, 0.0),
                           box_size=((x_end-self.L_in), self.ww+self.w_trench*2.0))

        for i in range(N):
            pts_core.append((x0, -(self.ww - dw_list[N-i-1]) / 2.0))
            pts_core.append((x0 - period_list[N-i-1] / 2.0, -(self.ww - dw_list[N-i-1]) / 2.0))
            pts_core.append((x0 - period_list[N-i-1] / 2.0, -self.ww / 2.0))
            pts_core.append((x0 - period_list[N-i-1], -self.ww / 2.0))
            x0 = x0 - period_list[N-i-1]

        # print(pts_core)

        elems += Boundary(layer=self.WGcore, shape=Shape(points=pts_core))

        x_shift = 0
        for i in range(self.N_end):

            elems += Rectangle(layer=self.WGcore, center=(x_end + self.end_period/4.0 + x_shift, 0.0),
                               box_size=(self.end_period/2.0, self.ww))
            x_shift = x_shift + self.end_period

        elems += Rectangle(layer=self.WGclad, center=(x_end + x_shift/2.0, 0.0),
                           box_size=(self.end_period*self.N_end, self.ww+self.w_trench*2.0))
        return elems


class EvaAntenna(Structure):
    __name_prefix__ = 'EvaAntenna'

    L1 = NumberProperty(default=0.204)
    L2 = NumberProperty(default=0.276)
    L3 = NumberProperty(default=0.0)
    L4 = NumberProperty(default=0.361)
    N_period = IntProperty(default=20)
    period = PositiveNumberProperty(default=0.8)
    w_port = PositiveNumberProperty(default=0.45)
    w_trench = PositiveNumberProperty(default=2.0)
    w_wg = PositiveNumberProperty(default=0.35)
    w_grating = PositiveNumberProperty(default=0.4)
    L_offset = NumberProperty(default=0.0)
    gap_end = PositiveNumberProperty(default=0.15)
    gap_start = PositiveNumberProperty(default=0.55)
    overlay = PositiveNumberProperty(default=0.05)
    L_extra = PositiveNumberProperty(default=2.0)
    w_slab = PositiveNumberProperty(default=4.0)
    L_taper = PositiveNumberProperty(default=10.0)
    resolution = IntProperty(default = 10)
    sk_slab = IntProperty(default=False)

    WGcore = PPLayer(process=TECH.PROCESS.WG, purpose=TECH.PURPOSE.LF.LINE)
    WGclad = PPLayer(process=TECH.PROCESS.WG, purpose=TECH.PURPOSE.LF_AREA)
    FCcore = PPLayer(process=TECH.PROCESS.FC, purpose=TECH.PURPOSE.LF.LINE)
    FCclad = PPLayer(process=TECH.PROCESS.FC, purpose=TECH.PURPOSE.LF_AREA)
    SKcore = PPLayer(process=TECH.PROCESS.SK, purpose=TECH.PURPOSE.LF.LINE)
    SKclad = PPLayer(process=TECH.PROCESS.SK, purpose=TECH.PURPOSE.LF_AREA)
    WGtrench = PPLayer(process=TECH.PROCESS.WG, purpose=TECH.PURPOSE.DF.TRENCH)


    def define_elements(self, elems):

        y_shift = Ybranch(out_sep=self.w_grating + self.gap_start * 2.0 + self.w_wg).size_info().width

        # add splitter
        elems += SRef(reference=Ybranch(out_sep=self.w_grating + self.gap_start * 2.0 + self.w_wg), position=(0.0, 0.0))

        if self.sk_slab:
            # add taper from splitter to waveguide
            trans = Transition(wg1=self.w_port, wg2=self.w_wg, wg3=1.2, w_sktrench=self.w_trench)
            L_trans = trans.size_info().width
            elems += SRef(reference=trans, position=(0.0, 0.0)).transform_copy(HMirror(mirror_plane_x=0.0) + Translation(
                (L_trans + y_shift, self.w_grating / 2.0 + self.gap_start + self.w_wg / 2.0)))
            elems += SRef(reference=trans, position=(0.0, 0.0)).transform_copy(HMirror(mirror_plane_x=0.0) + Translation(
                (L_trans + y_shift, -self.w_grating / 2.0 - self.gap_start - self.w_wg / 2.0)))



        else:
            trans = WireTaper(w_start=self.w_wg, w_end=self.w_port, taperlen=self.L_taper)
            L_trans = self.L_taper
            elems += SRef(reference=trans, position=(0.0, 0.0)).transform_copy(HMirror(mirror_plane_x=0.0) + Translation(
                (L_trans + y_shift, self.w_grating / 2.0 + self.gap_start + self.w_wg / 2.0)))
            elems += SRef(reference=trans, position=(0.0, 0.0)).transform_copy(HMirror(mirror_plane_x=0.0) + Translation(
                (L_trans + y_shift, -self.w_grating / 2.0 - self.gap_start - self.w_wg / 2.0)))


        period = self.L1+self.L2+self.L3+self.L4
        position1 = (L_trans + self.L_offset + self.L1 + self.L2/2.0 + y_shift + self.overlay*0.5, 0.0)
        position2 = (L_trans + self.L_offset + self.L1+self.L2+self.L3 / 2.0+y_shift, 0.0)
        position3 = (L_trans + self.L_offset + (self.L1+self.L2+self.L3) / 2.0+y_shift, 0.0)
        position4 = (L_trans + self.L_offset + period / 2.0+y_shift, 0.0)
        unit1 = Rectangle(layer=self.FCcore, center=position1, box_size=(self.L2+self.overlay*1.0, self.w_grating+self.overlay*2.0))
        if self.L3 > 0.0:
            unit2 = Rectangle(layer=self.FCcore, center=position2, box_size=(self.L3, self.w_grating+self.overlay*2.0))
        unit3 = Rectangle(layer=self.WGcore, center=position3, box_size=(self.L1+self.L2+self.L3, self.w_grating))
        unit4 = Rectangle(layer=self.FCclad, center=position4, box_size=(period, self.w_grating+self.overlay*2.0))
        grating = []
        for i in range(self.N_period):
            grating += unit1.transform_copy(transformation=Translation((period * i, 0.0)))
            if self.L3 > 0.0:
                grating += unit2.transform_copy(transformation=Translation((period * i, 0.0)))
            grating += unit3.transform_copy(transformation=Translation((period * i, 0.0)))
            grating += unit4.transform_copy(transformation=Translation((period * i, 0.0)))
            # print i





        # add grating units
        elems += grating
        if self.sk_slab:
            clad = self.SKclad
            core = self.SKcore

            elems += Rectangle(layer=self.WGtrench,
                               center=(L_trans + self.L_offset + (period * self.N_period) / 2.0+y_shift,
                                       self.w_slab/2.0+0.25),
                               box_size=((period * self.N_period+5.0), 0.5))

            elems += Rectangle(layer=self.WGtrench,
                               center=(L_trans + self.L_offset + (period * self.N_period) / 2.0+y_shift,
                                       -self.w_slab/2.0-0.25),
                               box_size=((period * self.N_period+5.0), 0.5))

            elems += Rectangle(layer=core,
                               center=(L_trans + self.L_offset + (period * self.N_period) / 2.0 + y_shift, 0.0),
                               box_size=((period * self.N_period),
                                         self.w_grating+2.0*self.overlay))

        else:
            clad = self.WGclad
            core = self.WGcore



        # add clad in grating region
        elems += Rectangle(layer=clad, center=(L_trans + self.L_offset + (period * self.N_period) / 2.0+y_shift, 0.0),
                           box_size=((period * self.N_period), self.w_wg*2.0+self.w_grating+self.gap_start*2.0+self.w_trench*2.0))



        # add waveguides in grating region
        z_list = np.linspace(start=0, stop=self.N_period * period, num=self.resolution, endpoint=True)
        pts_wg1 = []
        pts_wg2 = []
        para_a = self.gap_start
        para_b = np.log(self.gap_end / self.gap_start) / (self.N_period * period)
        for i in range(self.resolution):
            pts_wg1.append((L_trans + self.L_offset + z_list[i]+y_shift, self.w_grating / 2.0 + para_a * np.exp(para_b * z_list[i])))
            pts_wg2.append((L_trans + self.L_offset + z_list[i]+y_shift, -self.w_grating / 2.0 - para_a * np.exp(para_b * z_list[i])))
        for i in range(self.resolution):
            pts_wg1.append((L_trans + self.L_offset + z_list[self.resolution - i - 1]+y_shift, self.w_grating / 2.0 + para_a * np.exp(
                para_b * z_list[self.resolution - i - 1]) + self.w_wg))
            pts_wg2.append((L_trans + self.L_offset + z_list[self.resolution - i - 1]+y_shift, -self.w_grating / 2.0 - para_a * np.exp(
                para_b * z_list[self.resolution - i - 1]) - self.w_wg))

        # print pts_core
        elems += Boundary(layer=core, shape=Shape(points=pts_wg1))
        elems += Boundary(layer=core, shape=Shape(points=pts_wg2))



        # add waveguide stop
        elems += Rectangle(layer=clad, center=(L_trans + self.L_offset + (period * self.N_period)+ self.L_extra + y_shift, 0.0),
                           box_size=(self.L_extra*2.0, self.w_wg*2.0+self.w_grating+self.gap_start*2.0+self.w_trench*2.0))


        begin_x = L_trans + self.L_offset + (period * self.N_period) + y_shift
        y = self.w_grating / 2.0 + self.gap_end + self.w_wg / 2.0
        elems += Wedge(layer=core, begin_coord=(begin_x, y), end_coord=(begin_x+self.L_extra, y),
                       begin_width=self.w_wg, end_width=0.15)

        elems += Wedge(layer=core, begin_coord=(begin_x, -y), end_coord=(begin_x+self.L_extra, -y),
                       begin_width=self.w_wg, end_width=0.15)

        return elems


class EvaAntennaTestTree(Structure):
    __name_prefix__ = 'EvaAntennaTestTree'

    xn_start = ListProperty(default=np.arange(0, 32.0*4.0, 4.0).tolist())
    gap_start = ListProperty(default=np.linspace(0.3, 0.3, 32).tolist())
    gap_end = ListProperty(default=np.linspace(0.15, 0.15, 32).tolist())
    Nperiod = PositiveNumberProperty(default=310)

    # xn_start = ListProperty(default=np.arange(0, 16.0*20.0, 20).tolist())
    # gap_start = ListProperty(default=np.linspace(0.2, 0.8, 16).tolist())
    # gap_end = ListProperty(default=np.linspace(0.15, 0.15, 16).tolist())
    # Nperiod = PositiveNumberProperty(default=1500)


    M1_width = PositiveNumberProperty(default=0.6)
    M2_width = PositiveNumberProperty(default=0.9)
    FCW_width = PositiveNumberProperty(default=0.5)
    M1Layer = PPLayer(process=TECH.PROCESS.M1, purpose=TECH.PURPOSE.LF.ISLAND)
    M2Layer = PPLayer(process=TECH.PROCESS.M2, purpose=TECH.PURPOSE.LF.ISLAND)
    FCWLayer = PPLayer(process=TECH.PROCESS.FCW, purpose=TECH.PURPOSE.DF.TRENCH)
    M1process = ProcessProperty(default=TECH.PROCESS.M1)
    M2process = ProcessProperty(default=TECH.PROCESS.M2)
    FCWprocess = ProcessProperty(default=TECH.PROCESS.FCW)
    M1purpose = PurposeProperty(default=TECH.PURPOSE.LF.ISLAND)
    M2purpose = PurposeProperty(default=TECH.PURPOSE.LF.ISLAND)
    FCWpurpose = PurposeProperty(default=TECH.PURPOSE.DF.TRENCH)


    def define_elements(self, elems):
        N_channel = len(self.xn_start)
        elems += SRef(reference=SplitterTree(xn=self.xn_start, x_sep=80.0),
                      position=(-360+172-233.779+170.0+11.779-80.0-80.0,-15.0-111+108+18.0))
        for i in range(N_channel):
            antenna = EvaAntenna(N_period=self.Nperiod, gap_end=self.gap_end[i], gap_start=self.gap_start[i])

            elems += SRef(reference=antenna, position=(0.0, self.xn_start[i]))

        if self.xn_start[1] - self.xn_start[0] <= 5.0:
            L = antenna.size_info().width
            for i in range(N_channel - 1):
                M1_width = self.M1_width
                M2_width = self.M2_width
                FCW_width = self.FCW_width

                shift_dummy = 0.0

                elems += Rectangle(layer=self.M1Layer,
                                   center=(shift_dummy + L / 2.0, (self.xn_start[i] + self.xn_start[i + 1]) / 2.0),
                                   box_size=(L, M1_width))
                elems += Rectangle(layer=self.M2Layer,
                                   center=(shift_dummy + L / 2.0, (self.xn_start[i] + self.xn_start[i + 1]) / 2.0),
                                   box_size=(L, M2_width))
                elems += Rectangle(layer=self.FCWLayer,
                                   center=(shift_dummy + L / 2.0, (self.xn_start[i] + self.xn_start[i + 1]) / 2.0),
                                   box_size=(L, FCW_width))

                elems += Rectangle(layer=self.M1Layer,
                                   center=(
                                   shift_dummy + L / 2.0, (self.xn_start[i] + self.xn_start[i + 1]) / 2.0),
                                   box_size=(L, M1_width))
                elems += Rectangle(layer=self.M2Layer,
                                   center=(
                                   shift_dummy + L / 2.0, (self.xn_start[i] + self.xn_start[i + 1]) / 2.0),
                                   box_size=(L, M2_width))
                elems += Rectangle(layer=self.FCWLayer,
                                   center=(
                                   shift_dummy + L / 2.0, (self.xn_start[i] + self.xn_start[i + 1]) / 2.0),
                                   box_size=(L, FCW_width))

        return elems


class ReceiverMatrix(Structure):
    __name_prefix__ = 'ReceiverMatrix'

    pitch = PositiveNumberProperty(default=15.0)
    dimension1 = IntProperty(default=4)
    dimension2 = IntProperty(default=8)
    L_straight = PositiveNumberProperty(default=0.5)
    Receiver = DefinitionProperty()
    bend_radius = PositiveNumberProperty(default=6.0)
    w_port = PositiveNumberProperty(default=0.45)
    w_trench = PositiveNumberProperty(default=2.0)
    L_ext = PositiveNumberProperty(default=5.0)

    # layers
    WGcore = PPLayer(process=TECH.PROCESS.WG, purpose=TECH.PURPOSE.LF.LINE)
    WGclad = PPLayer(process=TECH.PROCESS.WG, purpose=TECH.PURPOSE.LF_AREA)

    def define_Receiver(self):
        Re = SRef(reference=ReceiverElement(L_straight=self.L_straight))
        return Re

    def define_elements(self, elems):

        for i in range(self.dimension1):


            for j in range(self.dimension1):
                elems += self.Receiver.transform_copy(HMirror(mirror_plane_x=0.0)+Translation((i*self.pitch+self.Receiver.size_info().width, j*self.pitch)))
                port = OpticalPort(position=(i*self.pitch+self.Receiver.size_info().width, j*self.pitch),
                                    angle=0,
                                    wg_definition=WgElDefinition(wg_width=self.w_port, trench_width=self.w_trench))

                # print(self.pitch/(self.dimension1))
                bend = RouteConnectorRounded(RouteToEastAtY(input_port=port, bend_radius=self.bend_radius, y_position=((self.dimension1-1-i)*self.pitch/(self.dimension1) + j*self.pitch), min_straight=1.0))
                elems += bend


                elems += SRef(reference=WireTaper(taperlen=(self.dimension1-1-i)*self.pitch-bend.size_info().width+self.L_ext),
                              position=(i*self.pitch+bend.size_info().width+self.Receiver.size_info().width,
                                        (self.dimension1-1-i)*self.pitch/(self.dimension1) + j*self.pitch))

            elems += Rectangle(layer=self.WGclad,
                               center=((self.pitch*(self.dimension1-1.0)+self.Receiver.size_info().width+self.L_ext)/2.0,
                                       self.pitch/self.dimension1*(self.dimension1**2-1)/2.0),
                               box_size=(self.pitch*(self.dimension1-1.0)+self.Receiver.size_info().width+self.L_ext,
                                         self.w_port+self.w_trench*2.0+self.pitch/self.dimension1*(self.dimension1**2-1)))

        return elems


class ReceiverOPA(Structure):
    __name_prefix__ = 'ReceiverOPA'

    # xn_start = ListProperty(default=np.arange(0, 4.0*64, 4.0).tolist())
    # xn_stop = ListProperty(default=np.arange(0, 1.875*64, 1.875).tolist())
    xn_start = ListProperty(default=np.arange(0, 4.0*16.0, 4.0).tolist())
    xn_stop = ListProperty(default=np.arange(0, 3.75*16.0, 3.75).tolist())
    bend_radius1 = PositiveNumberProperty(default=300)
    bend_radius2 = PositiveNumberProperty(default=300)
    w_port = PositiveNumberProperty(default=0.45)
    w_trench = PositiveNumberProperty(default=2.0)
    gap_heater = PositiveNumberProperty(default=12.0)
    L1 = PositiveNumberProperty(default=280.0)
    L2 = PositiveNumberProperty(default=320.0)
    L_heater = PositiveNumberProperty(default=204.6)

    M1_width = PositiveNumberProperty(default=0.6)
    M2_width = PositiveNumberProperty(default=0.9)
    FCW_width = PositiveNumberProperty(default=0.5)
    M1Layer = PPLayer(process=TECH.PROCESS.M1, purpose=TECH.PURPOSE.LF.ISLAND)
    M2Layer = PPLayer(process=TECH.PROCESS.M2, purpose=TECH.PURPOSE.LF.ISLAND)
    FCWLayer = PPLayer(process=TECH.PROCESS.FCW, purpose=TECH.PURPOSE.DF.TRENCH)
    M1process = ProcessProperty(default=TECH.PROCESS.M1)
    M2process = ProcessProperty(default=TECH.PROCESS.M2)
    FCWprocess = ProcessProperty(default=TECH.PROCESS.FCW)
    M1purpose = PurposeProperty(default=TECH.PURPOSE.LF.ISLAND)
    M2purpose = PurposeProperty(default=TECH.PURPOSE.LF.ISLAND)
    FCWpurpose = PurposeProperty(default=TECH.PURPOSE.DF.TRENCH)


    def define_elements(self, elems):
        tobe_connected1 = []
        tobe_connected2 = []
        N_channel = len(self.xn_start)
        for i in range(N_channel):
            coors_in = [0,self.xn_start[i]-np.mean(self.xn_start)]
            coors_H1 = [self.L1, self.gap_heater*i-self.gap_heater*N_channel/2.0]
            tobe_connected1 += [[coors_in, coors_H1]]

        for i in range(N_channel):
            coors_H2 = [self.L1+self.L_heater, self.gap_heater*i-self.gap_heater*N_channel/2.0]
            coors_out = [self.L1+self.L_heater+self.L2, self.xn_stop[i] - np.mean(self.xn_stop)]
            tobe_connected2 += [[coors_H2, coors_out]]
        L_bend1 = []
        L_bend2 = []

        for coors_pair1 in tobe_connected1:
            elems += SRef(SbendConnection(in_coor=coors_pair1[0], out_coor=coors_pair1[1], w_port=self.w_port,
                                          w_trench=self.gap_heater/2.0, bend_radius=self.bend_radius1))
            L_bend1.append(SbendConnection(in_coor=coors_pair1[0], out_coor=coors_pair1[1], w_port=self.w_port,
                                       w_trench=self.w_trench, bend_radius=self.bend_radius1).bend_length)

        for coors_pair2 in tobe_connected2:
            elems += SRef(SbendConnection(in_coor=coors_pair2[0], out_coor=coors_pair2[1], w_port=self.w_port,
                                          w_trench=self.gap_heater/2.0, bend_radius=self.bend_radius2))
            L_bend2.append(SbendConnection(in_coor=coors_pair2[0], out_coor=coors_pair2[1], w_port=self.w_port,
                                       w_trench=self.w_trench, bend_radius=self.bend_radius2).bend_length)



        tobe_connected3 = []
        tobe_connected4 = []
        N_channel = len(self.xn_start) - 1
        for i in range(N_channel):
            coors_in3 = [0, (self.xn_start[i] + self.xn_start[i + 1]) / 2.0 - np.mean(self.xn_start)]
            coors_H13 = [self.L1, self.gap_heater * i - self.gap_heater * N_channel / 2.0]
            tobe_connected3 += [[coors_in3, coors_H13]]

        for i in range(N_channel):
            coors_H23 = [self.L1 + self.L_heater, self.gap_heater * i - self.gap_heater * N_channel / 2.0]
            coors_out3 = [self.L1 + self.L_heater + self.L2,
                          (self.xn_stop[i] + self.xn_stop[i + 1]) / 2.0 - np.mean(self.xn_stop)]
            tobe_connected4 += [[coors_H23, coors_out3]]


        for coors_pair3 in tobe_connected3:
            elems += SRef(SbendConnectionFill(in_coor=coors_pair3[0], out_coor=coors_pair3[1], w_port=self.M1_width,
                                              process=self.M1process, purpose=self.M1purpose, bend_radius=self.bend_radius1))

            elems += SRef(SbendConnectionFill(in_coor=coors_pair3[0], out_coor=coors_pair3[1], w_port=self.M2_width,
                                              process=self.M2process, purpose=self.M2purpose, bend_radius=self.bend_radius1))

            elems += SRef(SbendConnectionFill(in_coor=coors_pair3[0], out_coor=coors_pair3[1], w_port=self.FCW_width,
                                              process=self.FCWprocess, purpose=self.FCWpurpose, bend_radius=self.bend_radius1))

        for coors_pair4 in tobe_connected4:
            elems += SRef(SbendConnectionFill(in_coor=coors_pair4[0], out_coor=coors_pair4[1], w_port=self.M1_width,
                                              process=self.M1process, purpose=self.M1purpose, bend_radius=self.bend_radius2))

            elems += SRef(SbendConnectionFill(in_coor=coors_pair4[0], out_coor=coors_pair4[1], w_port=self.M2_width,
                                              process=self.M2process, purpose=self.M2purpose, bend_radius=self.bend_radius2))

            elems += SRef(SbendConnectionFill(in_coor=coors_pair4[0], out_coor=coors_pair4[1], w_port=self.FCW_width,
                                              process=self.FCWprocess, purpose=self.FCWpurpose, bend_radius=self.bend_radius2))

            center = (coors_pair4[0][0] - self.L_heater / 2.0, coors_pair4[0][1])
            length = self.L_heater
            elems += Rectangle(layer=self.M1Layer,
                               center=center,
                               box_size=(length, self.M1_width))
            elems += Rectangle(layer=self.M2Layer,
                               center=center,
                               box_size=(length, self.M2_width))
            elems += Rectangle(layer=self.FCWLayer,
                               center=center,
                               box_size=(length, self.FCW_width))
        MMItree = SplitterTree(xn=self.xn_start, x_sep=65.0)
        L_MMItree = MMItree.size_info().width
        Lbend = np.max(L_bend1)+np.max(L_bend2)+self.L_heater
        ReMatrix = ReceiverMatrix(dimension1=4)
        elems += SRef(reference=MMItree, position=(-L_MMItree,-np.mean(self.xn_start)))
        x = ReMatrix.size_info().width+self.L1+self.L2+self.L_heater
        elems += SRef(reference=ReMatrix, transformation=HMirror(mirror_plane_x=0.0), position=(x, -np.mean(self.xn_stop)))

        return elems


class PolyText(Structure):
    __name_prefix__ = 'PolyText'
    text_list = ListProperty(default=['1', '2', '33', '17', 'TX1', 'TX2', 'TX3', 'TX4', 'RX1', 'RX2', 'RX3', 'RX4', 'RX5', 'TRX', 'Si', 'NN', 'PIN', 'MH', 'PP'])
    height = PositiveNumberProperty(default=8.0)
    textlayer = PPLayer(process=TECH.PROCESS.LOGOTXT, purpose=TECH.PURPOSE.DF_AREA)

    def define_elements(self, elems):
        for i in range(len(self.text_list)):
            elems += PolygonText(self.textlayer, self.text_list[i], (self.height / 2, 10.0*i), (TEXT_ALIGN_CENTER, TEXT_ALIGN_BOTTOM), 1, self.height)
        return elems


class PDKGratingCoupler(Structure):

    PDK_dir = "D:/GitFolder/PCL_codes/imec_202103/Imec2021_PDK/PDK_components/"

    GC = InputGdsii(file(PDK_dir+'grating_couplers/FGCCTE_FCWFC1DC_630_378.gds',"rb"))
    Layout = GC.read().top_layout()
    __name__ = Layout.name

    x_shift = DefinitionProperty()

    def define_elements(self, elems):
        elems = self.Layout.elements
        return elems

    def x_shift(self):
        return -30.40


class Test_GC(Structure):
    __name_prefix__ = 'Test_GC'
    L = PositiveNumberProperty(default=100.0)

    def define_elements(self, elems):
        x_shift = PDKGratingCoupler().x_shift()
        elems += SRef(PDKGratingCoupler(), (x_shift, 0))
        elems += SRef(WireTaper(taperlen=self.L, w_start=0.45, w_end =0.45),position=(0.0,0.0))
        elems += SRef(PDKGratingCoupler()).transform_copy(Translation((x_shift,0.0))+HMirror(mirror_plane_x=0.0)+Translation((self.L,0.0)))




        return elems


if __name__ == "__main__":
    print "Starting...."
    layout = Test_GC()
    # layout.visualize_2d()
    layout.write_gdsii("PDKGC.gds")
    print "Done : GDS2 file created."