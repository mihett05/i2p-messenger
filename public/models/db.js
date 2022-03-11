const { Sequelize } = require('sequelize');
const sqlite3 = require('sqlite3');

const sequelize = new Sequelize({
  dialect: 'sqlite',
  storage: 'storage.db',
});

module.exports = sequelize;
