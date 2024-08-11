import React, { useRef, useEffect } from 'react';
import ForceGraph3D from '3d-force-graph';
import * as THREE from 'three';


interface NodeObject {
    id: string;
    [key: string]: any;
  }
  
  interface LinkObject {
    source: string;
    target: string;
    [key: string]: any;
  }
  
  interface GraphData {
    nodes: NodeObject[];
    links: LinkObject[];
  }
  
  interface ForceGraphMethods {
    graphData(data: GraphData): this;
    nodeThreeObject(callback: (node: NodeObject) => THREE.Object3D): this;
    linkWidth(callback: (link: LinkObject) => number): this;
    onNodeClick(callback: (node: NodeObject) => void): this;
    [key: string]: any; // 他のメソッドのためのプロパティ
  }
  
  
  const Graph3D: React.FC = () => {
    const graphRef = useRef<HTMLDivElement>(null);
    const graph = useRef<any>(null);  // `any`型を使用
  
    useEffect(() => {
      if (graphRef.current) {
        graph.current = ForceGraph3D()(graphRef.current);
  
        // グラフのデータ
        graph.current.graphData({
          nodes: [
            { id: 'Node 1' },
            { id: 'Node 2' },
            { id: 'Node 3' }
          ],
          links: [
            { source: 'Node 1', target: 'Node 2' },
            { source: 'Node 2', target: 'Node 3' }
          ]
        });


        // リンクのカスタマイズ
        if (graph.current) {
            graph.current.linkWidth((link: any) => link.value || 2);  
            graph.current.linkColor(() => '#FFFFFF');
        }
  
        // ノードのカスタマイズ
        graph.current.nodeThreeObject((node: any) => {
          const sprite = new THREE.Sprite(new THREE.SpriteMaterial({ color: node.color || 0x00ff00 }));
          sprite.scale.set(8, 8, 8);
          return sprite;
        });
      }
  
      return () => {
        graph.current = null;
      };
    }, []);
  
    return <div ref={graphRef} style={{ width: '100%', height: '100vh' }} />;
  };
  
  export default Graph3D;
  