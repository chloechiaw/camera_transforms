import { useEffect, useState } from 'react';
import init, { ViewingCalculator } from './wasm/rust.js';

interface ComputeResult {
  platform: 'WASM' | 'Modal';
  result: number[];
  timeTaken: number;
}

export default function GraphicsCompute() {

  useEffect(() => {
    const initWasm = async () => {
      try {
        await init();
        console.log('WASM initialized successfully');
      } catch (error) {
        console.error('Failed to initialize WASM:', error);
      }
    };
    initWasm();
  }, []);

  const [dimensions, setDimensions] = useState({
    width: 1920,
    height: 1080,
    depth: 1000,
    points: 100000 
  });
  const [results, setResults] = useState<ComputeResult[]>([]);
  const [isComputing, setIsComputing] = useState(false);

  const runComputation = async () => {
    setIsComputing(true);

    try {
      const points = Array.from({ length: dimensions.points * 3 }, 
        () => Math.random() * 1000 - 500); 

      await init() 
      const wasmStart = performance.now();
      const calculator = new ViewingCalculator();
      const wasmResult = calculator.transform_points(
        new Float64Array(points),
        dimensions.width,
        dimensions.height,
        dimensions.depth
      );
      const wasmTime = performance.now() - wasmStart;
      console.log(wasmResult)

      const modalStart = performance.now();
      const modalResponse = await fetch('https://chloechiaw--compute-benchmark-transform-points-dev.modal.run', {
        method: 'POST',
        mode: 'cors',
        credentials: 'omit',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          points,
          width: dimensions.width,
          height: dimensions.height,
          depth: dimensions.depth
        })
      });

      if (!modalResponse.ok) {
        const errorText = await modalResponse.text();
        throw new Error(`API request failed: ${modalResponse.status} ${errorText}`);
      }

      const modalResult = await modalResponse.json();
      const modalTime = performance.now() - modalStart;

      setResults([
        {
          platform: 'WASM',
          result: Array.from(wasmResult),
          timeTaken: wasmTime
        },
        {
          platform: 'Modal',
          result: modalResult.points,
          timeTaken: modalTime
        }
      ]);
    } finally {
      setIsComputing(false);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">3D Point Transform Benchmark</h1>
      
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div>
          <label className="block mb-2">Number of Points:</label>
          <input
            type="number"
            value={dimensions.points}
            onChange={(e) => setDimensions(d => ({ ...d, points: Number(e.target.value) }))}
            className="w-full p-2 border rounded"
          />
        </div>
        
        <div>
          <label className="block mb-2">Viewport Size:</label>
          <div className="flex gap-2">
            <input
              type="number"
              value={dimensions.width}
              onChange={(e) => setDimensions(d => ({ ...d, width: Number(e.target.value) }))}
              className="w-full p-2 border rounded"
              placeholder="Width"
            />
            <input
              type="number"
              value={dimensions.height}
              onChange={(e) => setDimensions(d => ({ ...d, height: Number(e.target.value) }))}
              className="w-full p-2 border rounded"
              placeholder="Height"
            />
          </div>
        </div>
      </div>

      <button
        onClick={runComputation}
        disabled={isComputing}
        className="px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-400 mb-6"
      >
        {isComputing ? 'Computing...' : 'Run Computation'}
      </button>

      {results.length > 0 && (
        <div className="space-y-4">
          {results.map((result) => (
            <div key={result.platform} className="p-4 border rounded">
              <h2 className="font-bold">{result.platform}</h2>
              <p>Time: {result.timeTaken.toFixed(2)}ms</p>
              <p>First 5 transformed points:</p>
              <pre className="text-sm bg-gray-100 p-2 rounded">
                {result.result.slice(0, 15).map((n, i) => 
                  i % 3 === 0 ? `\n(${n.toFixed(2)}, ` : 
                  i % 3 === 1 ? `${n.toFixed(2)}, ` : 
                  `${n.toFixed(2)})`
                )}
              </pre>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}