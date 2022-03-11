const net = require('net');

class SocketClient {
  constructor(host, port) {
    this.socket = new net.Socket();
    this.socket.connect({ port, host }, () => {
      console.log(`Connected to ${host}:${port}`);
    });
    this.handlers = {};
    this.oneTimeHandlers = {};
    this.socket.on('data', (rawData) => {
      try {
        const data = JSON.parse(rawData);
        this.handlers[data.action]?.forEach((cb) => cb(data, this.send)); // calling every .on

        const handler = this.oneTimeHandlers[data.uid];
        if (handler) {
          handler(data, this.send);
          delete this.oneTimeHandlers[data.uid];
        }
      } catch (e) {
        // TODO: error handling
      }
    });
  }

  send(data) {
    this.socket.write(JSON.stringify(data));
  }

  on(action, cb) {
    if (!Object.keys(this.handlers).includes(action)) this.handlers[action] = [];
    this.handlers[action].push(cb);
  }

  once(uid, cb) {
    this.oneTimeHandlers[uid] = cb;
  }
}

module.exports = {
  SocketClient,
};
