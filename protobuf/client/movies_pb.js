/**
 * @fileoverview
 * @enhanceable
 * @suppress {messageConventions} JS Compiler reports an error if a variable or
 *     field starts with 'MSG_' and isn't a translatable message.
 * @public
 */
// GENERATED CODE -- DO NOT EDIT!

var jspb = require('google-protobuf');
var goog = jspb;
var global = Function('return this')();

goog.exportSymbol('proto.Command', null, global);
goog.exportSymbol('proto.Movie', null, global);
goog.exportSymbol('proto.MoviesList', null, global);

/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Command = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.Command.repeatedFields_, null);
};
goog.inherits(proto.Command, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  proto.Command.displayName = 'proto.Command';
}
/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.Command.repeatedFields_ = [2];



if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto suitable for use in Soy templates.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     com.google.apps.jspb.JsClassTemplate.JS_RESERVED_WORDS.
 * @param {boolean=} opt_includeInstance Whether to include the JSPB instance
 *     for transitional soy proto support: http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Command.prototype.toObject = function(opt_includeInstance) {
  return proto.Command.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Command} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Command.toObject = function(includeInstance, msg) {
  var f, obj = {
    cmd: jspb.Message.getFieldWithDefault(msg, 1, ""),
    argsList: jspb.Message.getRepeatedField(msg, 2)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Command}
 */
proto.Command.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Command;
  return proto.Command.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Command} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Command}
 */
proto.Command.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setCmd(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.addArgs(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Command.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Command.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Command} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Command.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getCmd();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getArgsList();
  if (f.length > 0) {
    writer.writeRepeatedString(
      2,
      f
    );
  }
};


/**
 * optional string cmd = 1;
 * @return {string}
 */
proto.Command.prototype.getCmd = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/** @param {string} value */
proto.Command.prototype.setCmd = function(value) {
  jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * repeated string args = 2;
 * @return {!Array<string>}
 */
proto.Command.prototype.getArgsList = function() {
  return /** @type {!Array<string>} */ (jspb.Message.getRepeatedField(this, 2));
};


/** @param {!Array<string>} value */
proto.Command.prototype.setArgsList = function(value) {
  jspb.Message.setField(this, 2, value || []);
};


/**
 * @param {!string} value
 * @param {number=} opt_index
 */
proto.Command.prototype.addArgs = function(value, opt_index) {
  jspb.Message.addToRepeatedField(this, 2, value, opt_index);
};


proto.Command.prototype.clearArgsList = function() {
  this.setArgsList([]);
};



/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Movie = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.Movie.repeatedFields_, null);
};
goog.inherits(proto.Movie, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  proto.Movie.displayName = 'proto.Movie';
}
/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.Movie.repeatedFields_ = [3,6,12,13,14,15];



if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto suitable for use in Soy templates.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     com.google.apps.jspb.JsClassTemplate.JS_RESERVED_WORDS.
 * @param {boolean=} opt_includeInstance Whether to include the JSPB instance
 *     for transitional soy proto support: http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Movie.prototype.toObject = function(opt_includeInstance) {
  return proto.Movie.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Movie} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Movie.toObject = function(includeInstance, msg) {
  var f, obj = {
    id: jspb.Message.getFieldWithDefault(msg, 1, ""),
    plot: jspb.Message.getFieldWithDefault(msg, 2, ""),
    genresList: jspb.Message.getRepeatedField(msg, 3),
    runtime: jspb.Message.getFieldWithDefault(msg, 4, 0),
    rated: jspb.Message.getFieldWithDefault(msg, 5, ""),
    castList: jspb.Message.getRepeatedField(msg, 6),
    poster: jspb.Message.getFieldWithDefault(msg, 7, ""),
    title: jspb.Message.getFieldWithDefault(msg, 8, ""),
    fullplot: jspb.Message.getFieldWithDefault(msg, 9, ""),
    year: jspb.Message.getFieldWithDefault(msg, 10, 0),
    type: jspb.Message.getFieldWithDefault(msg, 11, ""),
    writersList: jspb.Message.getRepeatedField(msg, 12),
    countriesList: jspb.Message.getRepeatedField(msg, 13),
    languagesList: jspb.Message.getRepeatedField(msg, 14),
    directorsList: jspb.Message.getRepeatedField(msg, 15)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Movie}
 */
proto.Movie.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Movie;
  return proto.Movie.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Movie} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Movie}
 */
proto.Movie.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setId(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setPlot(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.addGenres(value);
      break;
    case 4:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setRuntime(value);
      break;
    case 5:
      var value = /** @type {string} */ (reader.readString());
      msg.setRated(value);
      break;
    case 6:
      var value = /** @type {string} */ (reader.readString());
      msg.addCast(value);
      break;
    case 7:
      var value = /** @type {string} */ (reader.readString());
      msg.setPoster(value);
      break;
    case 8:
      var value = /** @type {string} */ (reader.readString());
      msg.setTitle(value);
      break;
    case 9:
      var value = /** @type {string} */ (reader.readString());
      msg.setFullplot(value);
      break;
    case 10:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setYear(value);
      break;
    case 11:
      var value = /** @type {string} */ (reader.readString());
      msg.setType(value);
      break;
    case 12:
      var value = /** @type {string} */ (reader.readString());
      msg.addWriters(value);
      break;
    case 13:
      var value = /** @type {string} */ (reader.readString());
      msg.addCountries(value);
      break;
    case 14:
      var value = /** @type {string} */ (reader.readString());
      msg.addLanguages(value);
      break;
    case 15:
      var value = /** @type {string} */ (reader.readString());
      msg.addDirectors(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Movie.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Movie.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Movie} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Movie.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getId();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getPlot();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getGenresList();
  if (f.length > 0) {
    writer.writeRepeatedString(
      3,
      f
    );
  }
  f = message.getRuntime();
  if (f !== 0) {
    writer.writeInt32(
      4,
      f
    );
  }
  f = message.getRated();
  if (f.length > 0) {
    writer.writeString(
      5,
      f
    );
  }
  f = message.getCastList();
  if (f.length > 0) {
    writer.writeRepeatedString(
      6,
      f
    );
  }
  f = message.getPoster();
  if (f.length > 0) {
    writer.writeString(
      7,
      f
    );
  }
  f = message.getTitle();
  if (f.length > 0) {
    writer.writeString(
      8,
      f
    );
  }
  f = message.getFullplot();
  if (f.length > 0) {
    writer.writeString(
      9,
      f
    );
  }
  f = message.getYear();
  if (f !== 0) {
    writer.writeInt32(
      10,
      f
    );
  }
  f = message.getType();
  if (f.length > 0) {
    writer.writeString(
      11,
      f
    );
  }
  f = message.getWritersList();
  if (f.length > 0) {
    writer.writeRepeatedString(
      12,
      f
    );
  }
  f = message.getCountriesList();
  if (f.length > 0) {
    writer.writeRepeatedString(
      13,
      f
    );
  }
  f = message.getLanguagesList();
  if (f.length > 0) {
    writer.writeRepeatedString(
      14,
      f
    );
  }
  f = message.getDirectorsList();
  if (f.length > 0) {
    writer.writeRepeatedString(
      15,
      f
    );
  }
};


/**
 * optional string id = 1;
 * @return {string}
 */
proto.Movie.prototype.getId = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/** @param {string} value */
proto.Movie.prototype.setId = function(value) {
  jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string plot = 2;
 * @return {string}
 */
proto.Movie.prototype.getPlot = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/** @param {string} value */
proto.Movie.prototype.setPlot = function(value) {
  jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * repeated string genres = 3;
 * @return {!Array<string>}
 */
proto.Movie.prototype.getGenresList = function() {
  return /** @type {!Array<string>} */ (jspb.Message.getRepeatedField(this, 3));
};


/** @param {!Array<string>} value */
proto.Movie.prototype.setGenresList = function(value) {
  jspb.Message.setField(this, 3, value || []);
};


/**
 * @param {!string} value
 * @param {number=} opt_index
 */
proto.Movie.prototype.addGenres = function(value, opt_index) {
  jspb.Message.addToRepeatedField(this, 3, value, opt_index);
};


proto.Movie.prototype.clearGenresList = function() {
  this.setGenresList([]);
};


/**
 * optional int32 runtime = 4;
 * @return {number}
 */
proto.Movie.prototype.getRuntime = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 4, 0));
};


/** @param {number} value */
proto.Movie.prototype.setRuntime = function(value) {
  jspb.Message.setProto3IntField(this, 4, value);
};


/**
 * optional string rated = 5;
 * @return {string}
 */
proto.Movie.prototype.getRated = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 5, ""));
};


/** @param {string} value */
proto.Movie.prototype.setRated = function(value) {
  jspb.Message.setProto3StringField(this, 5, value);
};


/**
 * repeated string cast = 6;
 * @return {!Array<string>}
 */
proto.Movie.prototype.getCastList = function() {
  return /** @type {!Array<string>} */ (jspb.Message.getRepeatedField(this, 6));
};


/** @param {!Array<string>} value */
proto.Movie.prototype.setCastList = function(value) {
  jspb.Message.setField(this, 6, value || []);
};


/**
 * @param {!string} value
 * @param {number=} opt_index
 */
proto.Movie.prototype.addCast = function(value, opt_index) {
  jspb.Message.addToRepeatedField(this, 6, value, opt_index);
};


proto.Movie.prototype.clearCastList = function() {
  this.setCastList([]);
};


/**
 * optional string poster = 7;
 * @return {string}
 */
proto.Movie.prototype.getPoster = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 7, ""));
};


/** @param {string} value */
proto.Movie.prototype.setPoster = function(value) {
  jspb.Message.setProto3StringField(this, 7, value);
};


/**
 * optional string title = 8;
 * @return {string}
 */
proto.Movie.prototype.getTitle = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 8, ""));
};


/** @param {string} value */
proto.Movie.prototype.setTitle = function(value) {
  jspb.Message.setProto3StringField(this, 8, value);
};


/**
 * optional string fullplot = 9;
 * @return {string}
 */
proto.Movie.prototype.getFullplot = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 9, ""));
};


/** @param {string} value */
proto.Movie.prototype.setFullplot = function(value) {
  jspb.Message.setProto3StringField(this, 9, value);
};


/**
 * optional int32 year = 10;
 * @return {number}
 */
proto.Movie.prototype.getYear = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 10, 0));
};


/** @param {number} value */
proto.Movie.prototype.setYear = function(value) {
  jspb.Message.setProto3IntField(this, 10, value);
};


/**
 * optional string type = 11;
 * @return {string}
 */
proto.Movie.prototype.getType = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 11, ""));
};


/** @param {string} value */
proto.Movie.prototype.setType = function(value) {
  jspb.Message.setProto3StringField(this, 11, value);
};


/**
 * repeated string writers = 12;
 * @return {!Array<string>}
 */
proto.Movie.prototype.getWritersList = function() {
  return /** @type {!Array<string>} */ (jspb.Message.getRepeatedField(this, 12));
};


/** @param {!Array<string>} value */
proto.Movie.prototype.setWritersList = function(value) {
  jspb.Message.setField(this, 12, value || []);
};


/**
 * @param {!string} value
 * @param {number=} opt_index
 */
proto.Movie.prototype.addWriters = function(value, opt_index) {
  jspb.Message.addToRepeatedField(this, 12, value, opt_index);
};


proto.Movie.prototype.clearWritersList = function() {
  this.setWritersList([]);
};


/**
 * repeated string countries = 13;
 * @return {!Array<string>}
 */
proto.Movie.prototype.getCountriesList = function() {
  return /** @type {!Array<string>} */ (jspb.Message.getRepeatedField(this, 13));
};


/** @param {!Array<string>} value */
proto.Movie.prototype.setCountriesList = function(value) {
  jspb.Message.setField(this, 13, value || []);
};


/**
 * @param {!string} value
 * @param {number=} opt_index
 */
proto.Movie.prototype.addCountries = function(value, opt_index) {
  jspb.Message.addToRepeatedField(this, 13, value, opt_index);
};


proto.Movie.prototype.clearCountriesList = function() {
  this.setCountriesList([]);
};


/**
 * repeated string languages = 14;
 * @return {!Array<string>}
 */
proto.Movie.prototype.getLanguagesList = function() {
  return /** @type {!Array<string>} */ (jspb.Message.getRepeatedField(this, 14));
};


/** @param {!Array<string>} value */
proto.Movie.prototype.setLanguagesList = function(value) {
  jspb.Message.setField(this, 14, value || []);
};


/**
 * @param {!string} value
 * @param {number=} opt_index
 */
proto.Movie.prototype.addLanguages = function(value, opt_index) {
  jspb.Message.addToRepeatedField(this, 14, value, opt_index);
};


proto.Movie.prototype.clearLanguagesList = function() {
  this.setLanguagesList([]);
};


/**
 * repeated string directors = 15;
 * @return {!Array<string>}
 */
proto.Movie.prototype.getDirectorsList = function() {
  return /** @type {!Array<string>} */ (jspb.Message.getRepeatedField(this, 15));
};


/** @param {!Array<string>} value */
proto.Movie.prototype.setDirectorsList = function(value) {
  jspb.Message.setField(this, 15, value || []);
};


/**
 * @param {!string} value
 * @param {number=} opt_index
 */
proto.Movie.prototype.addDirectors = function(value, opt_index) {
  jspb.Message.addToRepeatedField(this, 15, value, opt_index);
};


proto.Movie.prototype.clearDirectorsList = function() {
  this.setDirectorsList([]);
};



/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.MoviesList = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.MoviesList.repeatedFields_, null);
};
goog.inherits(proto.MoviesList, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  proto.MoviesList.displayName = 'proto.MoviesList';
}
/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.MoviesList.repeatedFields_ = [1];



if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto suitable for use in Soy templates.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     com.google.apps.jspb.JsClassTemplate.JS_RESERVED_WORDS.
 * @param {boolean=} opt_includeInstance Whether to include the JSPB instance
 *     for transitional soy proto support: http://goto/soy-param-migration
 * @return {!Object}
 */
proto.MoviesList.prototype.toObject = function(opt_includeInstance) {
  return proto.MoviesList.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.MoviesList} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.MoviesList.toObject = function(includeInstance, msg) {
  var f, obj = {
    moviesList: jspb.Message.toObjectList(msg.getMoviesList(),
    proto.Movie.toObject, includeInstance)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.MoviesList}
 */
proto.MoviesList.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.MoviesList;
  return proto.MoviesList.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.MoviesList} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.MoviesList}
 */
proto.MoviesList.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = new proto.Movie;
      reader.readMessage(value,proto.Movie.deserializeBinaryFromReader);
      msg.addMovies(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.MoviesList.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.MoviesList.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.MoviesList} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.MoviesList.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getMoviesList();
  if (f.length > 0) {
    writer.writeRepeatedMessage(
      1,
      f,
      proto.Movie.serializeBinaryToWriter
    );
  }
};


/**
 * repeated Movie movies = 1;
 * @return {!Array<!proto.Movie>}
 */
proto.MoviesList.prototype.getMoviesList = function() {
  return /** @type{!Array<!proto.Movie>} */ (
    jspb.Message.getRepeatedWrapperField(this, proto.Movie, 1));
};


/** @param {!Array<!proto.Movie>} value */
proto.MoviesList.prototype.setMoviesList = function(value) {
  jspb.Message.setRepeatedWrapperField(this, 1, value);
};


/**
 * @param {!proto.Movie=} opt_value
 * @param {number=} opt_index
 * @return {!proto.Movie}
 */
proto.MoviesList.prototype.addMovies = function(opt_value, opt_index) {
  return jspb.Message.addToRepeatedWrapperField(this, 1, opt_value, proto.Movie, opt_index);
};


proto.MoviesList.prototype.clearMoviesList = function() {
  this.setMoviesList([]);
};


goog.object.extend(exports, proto);