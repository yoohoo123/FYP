import React from 'react';
import io from 'socket.io-client';
import AntProgress from './progress';
import Markdown from './markdown';
import AntSlider from './slider';
import Dropdown from './dropdown';
import AntTable from './table';
import Bowhead from './header';
import PlotlyPlot from './plotly';

export const socket = io({path: '/socket.io'});

export const components = {
    1: <Markdown initial={'<h1>Bowtie Demo</h1>\n<p>Demonstrates interactive elements with the iris dataset.\nSelect some attributes to plot and select some data on the 2d plot.\nChange the alpha parameter to see how that affects the model.</p>'} socket={socket} uuid={'1'} />,
    2: <Dropdown initOptions={[{"value": "Sepal.Length", "label": "Sepal.Length"}, {"value": "Sepal.Width", "label": "Sepal.Width"}, {"value": "Petal.Length", "label": "Petal.Length"}, {"value": "Petal.Width", "label": "Petal.Width"}]} multi={false} default={null} socket={socket} uuid={'2'} />,
    3: <Dropdown initOptions={[{"value": "Sepal.Length", "label": "Sepal.Length"}, {"value": "Sepal.Width", "label": "Sepal.Width"}, {"value": "Petal.Length", "label": "Petal.Length"}, {"value": "Petal.Width", "label": "Petal.Width"}]} multi={false} default={null} socket={socket} uuid={'3'} />,
    4: <Dropdown initOptions={[{"value": "Sepal.Length", "label": "Sepal.Length"}, {"value": "Sepal.Width", "label": "Sepal.Width"}, {"value": "Petal.Length", "label": "Petal.Length"}, {"value": "Petal.Width", "label": "Petal.Width"}]} multi={false} default={null} socket={socket} uuid={'4'} />,
    5: <AntSlider range={false} min={1} max={50} step={1} start={10} marks={{1: '1', 50: '50'}} vertical={false} socket={socket} uuid={'5'} />,
    7: <AntProgress socket={socket} uuid={'6'}><PlotlyPlot initState={{"data": [], "layout": {"autosize": false}}} socket={socket} uuid={'7'} /></AntProgress>,
    9: <AntProgress socket={socket} uuid={'8'}><PlotlyPlot initState={{"data": [], "layout": {"autosize": false}}} socket={socket} uuid={'9'} /></AntProgress>,
    11: <AntProgress socket={socket} uuid={'10'}><PlotlyPlot initState={{"data": [], "layout": {"autosize": false}}} socket={socket} uuid={'11'} /></AntProgress>,
    13: <AntProgress socket={socket} uuid={'12'}><AntTable columns={[]} resultsPerPage={10} socket={socket} uuid={'13'} /></AntProgress>,
    14: <Bowhead initial={'X Variable'} size={3} socket={socket} uuid={'14'} />,
    15: <Bowhead initial={'Y Variable'} size={3} socket={socket} uuid={'15'} />,
    16: <Bowhead initial={'Z Variable'} size={3} socket={socket} uuid={'16'} />,
    17: <Bowhead initial={'Alpha Parameter'} size={3} socket={socket} uuid={'17'} />,
};