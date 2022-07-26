const webpack = require('webpack');
var path = require('path');
var CompressionPlugin = require('compression-webpack-plugin');

var BUILD_DIR = path.resolve(__dirname);
var APP_DIR = path.resolve(__dirname, 'bowtiejs');

var config = {
    context: __dirname,
    entry: APP_DIR + '/index.jsx',
    output: {
        path: BUILD_DIR,
        filename: 'bundle.js'
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                include: APP_DIR,
                loader: 'babel-loader',
                exclude: /node_modules/,
                options: {
                    presets: [
                        ['@babel/preset-env', {'modules': false}],
                        '@babel/preset-react'],
                    plugins: [
                        ['babel-plugin-import', {'libraryName': 'antd', 'style': true}],
                        '@babel/plugin-proposal-object-rest-spread',
                        '@babel/plugin-proposal-class-properties',
                    ],
                    babelrc: false
                }
            }, {
                test: /\.scss$/,
                loaders: ['style-loader', 'css-loader', 'sass-loader'],
            }, {
                test: /\.css$/,
                loader: 'style-loader!css-loader!sass-loader',
            }, {
                test: /\.less$/,
                use: [
                    {loader: "style-loader"},
                    {loader: "css-loader"},
                    {loader: "less-loader",
                        options: {
                            strictMath: false,
                            javascriptEnabled: true,
                            noIeCompat: true,
                            root: path.resolve(__dirname, './')
                        }
                    }
                ]
            },
        ],
        noParse: [
            /plotly\.js$/
        ],
    },
    resolve: {
        extensions: ['.jsx', '.js', '.json'],
        modules: [
            path.resolve(__dirname, APP_DIR), 'node_modules'
        ]
    }
};

module.exports = config;