from aiohttp import web
import asyncio
from ws2812_driver import Ws2812Driver
import numpy as np
import yaml


class Ws2812ApiServer():

    def __init__(self, settings):

        data = settings
        num_leds = data['ws2812_config']['num_leds']
        self.ws_strip = Ws2812Driver(num_leds)
        self.layers = []
        self.layer = dict()

        for layer in data['layers']:
            layer['mark'] = 0
            self.layers.append(layer)

        print("Imported layers from .yaml file")

        for i in range(len(self.layers)):
            print(self.layers[i]["name"])

    async def create_layer(self, request):
        """
        POST create new layer for driver
        http://0.0.0.0:8080/layers/{name}/set
        """
        data = await request.json()
        name = request.match_info['name']

        origin = data["origin"]
        leds = data["leds"]
        alpha = data["alpha"]

        x = 0

        for value in range(len(self.layers)):
            if self.layers[value]["name"] == name:
                x = 1
                order = value
        layer = {}
        if x == 0:
            layer['name'] = name
            layer['origin'] = origin
            layer['leds'] = leds
            layer['alpha'] = alpha
            layer['mark'] = 0
            self.layers.append(layer)
        else:
            layer[order]['leds'] = leds
            layer[order]['alpha'] = alpha
            layer[order]['origin'] = origin

        print("Actual layers:")
        for i in range(len(self.layers)):
            print(self.layers[i]["name"])

        return web.Response(text="New layers were succesfully uploaded.", status=200)

    async def show_scale(self, request):
        """
        POST upload parameters to show_scale
        http://0.0.0.0:8080/layers/{name}/show_scale
        """
        param = await request.json()
        name = request.match_info['name']

        min, max, temp = param["min"], param["max"], param["temp"]
        bright = param["bright"]
        reverse = param["reverse"]
        heatmap = param["heatmap"]

        if param["heatmap"] == 0:

            newmap = None

        else:

            newmap = []
            for i in range(len(heatmap)):
                min_ra, max_ra = heatmap[i]['min'], heatmap[i]['max']
                red = heatmap[i]['colour'][0]
                green = heatmap[i]['colour'][1]
                blue = heatmap[i]['colour'][2]
                newmap.append(tuple((min_ra, max_ra, tuple((red, green, blue)))))

        for value in range(len(self.layers)):
            if self.layers[value]["name"] == name:
                order = value

        if self.layers[order]['mark'] == 0:
            origin = self.layers[order]["origin"]
            leds = self.layers[order]["leds"]
            alpha = self.layers[order]["alpha"]

            self.layer[order] = self.ws_strip.add_segment(origin, leds, alpha)
            self.layers[order]["mark"] = 1
            self.layer[order].show_scale(min, max, temp, bright=bright, heatmap=newmap, reverse=reverse)

        else:

            self.layer[order].show_scale(min, max, temp, bright=bright,heatmap=newmap, reverse=reverse)

        return web.json_response(
            {'Status': 'New show_scale was succesfully uploaded.'}, status=200)

        return web.Response(text="New show_scale was sucesfully uploaded", status=200)

    async def show_raw(self, request):
        """
        POST upload parameters to show_raw
        0.0.0.0:8080/layers/{name}/show_raw
        """
        param = await request.json()

        name = request.match_info['name']

        for value in range(len(self.layers)):                               # find order in dict parameter to set layer
            if self.layers[value]["name"] == name:
                order = value
                leds = self.layers[value]["leds"]

        red =  param["red"]
        blue = param["blue"]
        green = param["green"]

        pixels = np.array(leds * [[red, blue, green]])
        print(pixels)

        if self.layers[order]['mark'] == 0:                                 # if new layer is not set up
            origin = self.layers[order]["origin"]
            leds = self.layers[order]["leds"]
            alpha = self.layers[order]["alpha"]

            self.layer[order] = self.ws_strip.add_segment(origin, leds, alpha)
            self.layers[order]["mark"] = 1
            self.layer[order].show_raw(pixels)
        else:
            self.layer[order].show_raw(pixels)

        return web.Response(text="New show_raw was succesfully uploaded", status=200)

    async def show_animation(self,request):
        """POST upload parameters to show_animation
        0.0.0.0:8080/layers/{names}/show_animation
        """
        param = await request.json()
        print('Param for show_animation:')
        print(param)

        name = request.match_info['name']
        speed =  param["speed"]

        for value in range(len(self.layers)):       # find order in dict parameter to set layer
            if self.layers[value]["name"] == name:
                order = value                       # set layer num.

        origin = self.layers[order]["origin"]
        leds = self.layers[order]["leds"]
        alpha = self.layers[order]["alpha"]

        self.layer[order] = self.ws_strip.add_segment(origin, leds, alpha)
        self.layer[order].show_animation(speed)

        return web.Response(text='New show_animation was succesfully uploaded.', status=200)

    def run(self, host='0.0.0.0', port=8080):

        app = web.Application()

        app.router.add_route('POST', '/layers/{name}/set', self.create_layer)
        app.router.add_route('POST', '/layers/{name}/show_scale', self.show_scale)
        app.router.add_route('POST', '/layers/{name}/show_raw', self.show_raw)
        app.router.add_route('POST', '/layers/{name}/show_animation', self.show_animation)

        loop = asyncio.get_event_loop()
        handler = app.make_handler()
        f = loop.create_server(handler, host=host, port=port)
        srv = loop.run_until_complete(f)

        loop.run_forever()
        code.interact(local=locals())

if __name__ == "__main__":


    with open("settings.yaml", 'r') as config_file:  # open of yaml file
        settings = yaml.load(config_file)            # load data

    srv = Ws2812ApiServer(settings=settings)
    srv.run(host='0.0.0.0', port=8080)
