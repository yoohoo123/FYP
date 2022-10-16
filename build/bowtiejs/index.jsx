import 'normalize.css';
import React from 'react';
import ReactDOM from 'react-dom';
import { message } from 'antd';
import {
    BrowserRouter,
    Switch,
    Route,
    Link
} from 'react-router-dom';

import { View } from './view';
import { socket } from './components';

var msgpack = require('msgpack-lite');

class Dashboard extends React.Component {
    constructor(props) {
        super(props);
        this.cache = {};
        socket.emit('INITIALIZE');
    }

    saveValue = data => {
        var arr = new Uint8Array(data['key']);
        var key = msgpack.decode(arr);
        var value = new Uint8Array(data['data']).toString();
        sessionStorage.setItem('cache' + key, value);
    }

    loadValue = (data, fn) => {
        var arr = new Uint8Array(data['data']);
        var key = msgpack.decode(arr);
        var x = sessionStorage.getItem('cache' + key)
        if (x === null) {
            var buffer = new ArrayBuffer(1);
            var x = new DataView(buffer, 0);
            // msgpack encodes null to 0xc0
            x.setUint8(0, 0xc0);
            fn(buffer);
        } else {
            x = new Uint8Array(x.split(','));
            fn(x.buffer);
        }
    }

    componentDidMount() {
        socket.on('cache_save', this.saveValue);
        socket.on('cache_load', this.loadValue);
        socket.on('message.success', (data) => {
            var arr = new Uint8Array(data['data']);
            message.success(msgpack.decode(arr));
        });
        socket.on('message.error', (data) => {
            var arr = new Uint8Array(data['data']);
            message.error(msgpack.decode(arr));
        });
        socket.on('message.info', (data) => {
            var arr = new Uint8Array(data['data']);
            message.info(msgpack.decode(arr));
        });
        socket.on('message.warning', (data) => {
            var arr = new Uint8Array(data['data']);
            message.warning(msgpack.decode(arr));
        });
        socket.on('message.loading', (data) => {
            var arr = new Uint8Array(data['data']);
            message.loading(msgpack.decode(arr));
        });
    }

    render() {
        return (
            <BrowserRouter>
                <Switch>
                        <Route
                            exact
                            path='/'
                            render={() => 
                                    <View
                                        uuid={'1'}
                                        background_color={'PaleTurquoise'}
                                        columns={'18em 2fr 1fr 1fr'}
                                        rows={'1fr 1fr'}
                                        column_gap={'0px'}
                                        row_gap={'0px'}
                                        border={'7px'}
                                        spans={{
                                           '1,1,2,2': [
                                                7,
                                           ],
                                           '1,2,2,4': [
                                                9,
                                           ],
                                           '2,1,3,3': [
                                                11,
                                           ],
                                           '2,3,3,4': [
                                                13,
                                           ],
                                        }}
                                        controllers={[ 
                                            1,
                                            14,
                                            2,
                                            15,
                                            3,
                                            16,
                                            4,
                                            17,
                                            5,
                                        ]}
                                        sidebar={ true }
                                    />
                            }
                        />
                </Switch>
            </BrowserRouter>
        );
    }
}

ReactDOM.render(<Dashboard />, document.getElementById('app'));