// Patched version of THREE.PLYLoader.js for full custom attribute support
// Based on: https://unpkg.com/three@0.160.1/examples/jsm/loaders/PLYLoader.js

import {
  BufferAttribute,
  BufferGeometry,
  FileLoader,
  Loader
} from 'three';

class PLYLoader extends Loader {

  constructor(manager) {
    super(manager);
  }

  load(url, onLoad, onProgress, onError) {
    const loader = new FileLoader(this.manager);
    loader.setPath(this.path);
    loader.setResponseType('arraybuffer');
    loader.setRequestHeader(this.requestHeader);
    loader.setWithCredentials(this.withCredentials);
    loader.load(url, (data) => {
      try {
        onLoad(this.parse(data));
      } catch (e) {
        if (onError) onError(e);
        else console.error(e);
        this.manager.itemError(url);
      }
    }, onProgress, onError);
  }

  parse(data) {
    function isASCII(data) {
      const header = parseHeader(bin2str(data));
      return header.format === 'ascii';
    }

    function bin2str(buf) {
      return new TextDecoder().decode(new Uint8Array(buf));
    }

    const scope = this;
    const geometry = new BufferGeometry();

    if (isASCII(data)) {
      return parseASCII(bin2str(data));
    } else {
      console.warn('PLYLoader: only ASCII PLY is supported in this patched version.');
      return geometry;
    }

    function parseHeader(data) {
      const patternHeader = /ply([\s\S]*)end_header\s/;
      const headerText = '';
      const headerLength = 0;
      const header = {
        comments: [],
        elements: [],
        headerLength: 0
      };

      const lines = data.split('\n');
      let currentElement;

      for (let i = 0; i < lines.length; i++) {
        let line = lines[i].trim();
        if (line === 'end_header') {
          header.headerLength = i + 1;
          break;
        }

        const lineValues = line.split(/\s+/);
        const lineType = lineValues.shift();

        switch (lineType) {
          case 'format':
            header.format = lineValues[0];
            header.version = lineValues[1];
            break;
          case 'comment':
            header.comments.push(lineValues.join(' '));
            break;
          case 'element':
            currentElement = {
              name: lineValues[0],
              count: parseInt(lineValues[1]),
              properties: []
            };
            header.elements.push(currentElement);
            break;
          case 'property':
            currentElement.properties.push({
              type: lineValues[0],
              name: lineValues[lineValues.length - 1]
            });
            break;
        }
      }

      return header;
    }

    function parseASCII(data) {
      const geometry = new BufferGeometry();
      const lines = data.split('\n');
      const header = parseHeader(data);
      const vertexElement = header.elements.find(e => e.name === 'vertex');
      const vertexCount = vertexElement.count;
      const vertexProperties = vertexElement.properties;

      const attributeArrays = {};
      vertexProperties.forEach(p => {
        attributeArrays[p.name] = new Float32Array(vertexCount);
      });

      const start = header.headerLength;
      for (let i = 0; i < vertexCount; i++) {
        const line = lines[start + i].trim();
        if (line === '') continue;
        const tokens = line.split(/\s+/);
        for (let j = 0; j < vertexProperties.length; j++) {
          const name = vertexProperties[j].name;
          attributeArrays[name][i] = parseFloat(tokens[j]);
        }
      }

      const position = new Float32Array(vertexCount * 3);
      for (let i = 0; i < vertexCount; i++) {
        position[i * 3 + 0] = attributeArrays['x'][i];
        position[i * 3 + 1] = attributeArrays['y'][i];
        position[i * 3 + 2] = attributeArrays['z'][i];
      }
      geometry.setAttribute('position', new BufferAttribute(position, 3));

      if ('nx' in attributeArrays && 'ny' in attributeArrays && 'nz' in attributeArrays) {
        const normal = new Float32Array(vertexCount * 3);
        for (let i = 0; i < vertexCount; i++) {
          normal[i * 3 + 0] = attributeArrays['nx'][i];
          normal[i * 3 + 1] = attributeArrays['ny'][i];
          normal[i * 3 + 2] = attributeArrays['nz'][i];
        }
        geometry.setAttribute('normal', new BufferAttribute(normal, 3));
      }

      // Add all other attributes
      for (const name in attributeArrays) {
        if (['x', 'y', 'z', 'nx', 'ny', 'nz', 'red', 'green', 'blue', 'alpha'].includes(name)) continue;
        geometry.setAttribute(name, new BufferAttribute(attributeArrays[name], 1));
      }

      return geometry;
    }
  }
}

export { PLYLoader };
