const { Model, DataTypes } = require('sequelize');
const sequelize = require('./db');

class Storage extends Model {}

Storage.init(
  {
    key: {
      type: DataTypes.STRING,
      allowNull: false,
      unique: true,
    },
    value: {
      type: DataTypes.STRING,
      allowNull: true,
    },
  },
  {
    sequelize,
    modelName: 'Storage',
    tableName: 'storage',
  },
);

module.exports = Storage;
