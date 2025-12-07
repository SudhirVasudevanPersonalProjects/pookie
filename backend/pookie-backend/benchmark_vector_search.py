"""Performance benchmark for FAISS vector search"""
import time
import numpy as np
from app.ml.vector_index import VectorIndex

def benchmark():
    print("=" * 70)
    print("FAISS Vector Search Performance Benchmark")
    print("=" * 70)

    # Test 1: Batch add performance (100k vectors - architecture requirement)
    print("\n1. Benchmarking batch add (100,000 vectors, 384-dim)...")
    index = VectorIndex(dimension=384)

    # Add in batches to avoid memory issues
    total_vectors = 100000
    batch_size = 10000
    total_add_time = 0

    for i in range(0, total_vectors, batch_size):
        embeddings = np.random.randn(batch_size, 384).astype(np.float32)
        something_ids = list(range(i + 1, i + batch_size + 1))

        start = time.time()
        index.add_batch(something_ids, embeddings)
        total_add_time += (time.time() - start) * 1000

    print(f"   ✓ Added {total_vectors:,} vectors in {total_add_time:.2f}ms ({total_add_time/total_vectors:.3f}ms per vector)")

    # Test 2: Single search performance
    print("\n2. Benchmarking single search (top_k=5)...")
    query = np.random.randn(384).astype(np.float32)

    # Warmup
    for _ in range(5):
        index.search(query, top_k=5)

    # Benchmark
    search_times = []
    for _ in range(100):
        start = time.time()
        results = index.search(query, top_k=5)
        search_times.append((time.time() - start) * 1000)

    avg_search = np.mean(search_times)
    p95_search = np.percentile(search_times, 95)
    p99_search = np.percentile(search_times, 99)

    print(f"   ✓ Average search time: {avg_search:.2f}ms")
    print(f"   ✓ P95 search time: {p95_search:.2f}ms")
    print(f"   ✓ P99 search time: {p99_search:.2f}ms")

    # Architecture requirement: <100ms for <100k vectors
    if avg_search < 100:
        print(f"   ✅ PASS: Meets <100ms requirement ({avg_search:.2f}ms avg)")
    else:
        print(f"   ❌ FAIL: Exceeds 100ms requirement ({avg_search:.2f}ms avg)")

    # Test 3: Save/load performance
    print("\n3. Benchmarking save/load operations...")
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "benchmark.faiss")

        # Save
        start = time.time()
        index.save(filepath)
        save_time = (time.time() - start) * 1000
        print(f"   ✓ Save time (1000 vectors): {save_time:.2f}ms")

        # Load
        new_index = VectorIndex(dimension=384)
        start = time.time()
        new_index.load(filepath)
        load_time = (time.time() - start) * 1000
        print(f"   ✓ Load time (1000 vectors): {load_time:.2f}ms")

    # Test 4: Varying top_k performance
    print("\n4. Benchmarking different top_k values...")
    for k in [1, 5, 10, 50]:
        times = []
        for _ in range(50):
            start = time.time()
            index.search(query, top_k=k)
            times.append((time.time() - start) * 1000)
        avg = np.mean(times)
        print(f"   ✓ top_k={k:2d}: {avg:.2f}ms avg")

    # Summary
    print("\n" + "=" * 70)
    print("BENCHMARK SUMMARY")
    print("=" * 70)
    print(f"Index size: {total_vectors:,} vectors (384-dim)")
    print(f"Batch add: {total_add_time:.2f}ms total, {total_add_time/total_vectors:.3f}ms per vector")
    print(f"Search (top_k=5): {avg_search:.2f}ms avg, {p95_search:.2f}ms p95, {p99_search:.2f}ms p99")
    print(f"Save: {save_time:.2f}ms")
    print(f"Load: {load_time:.2f}ms")
    print(f"\n🎯 Architecture requirement: <100ms search time for <100k vectors")
    print(f"Result: {'✅ PASS' if avg_search < 100 else '❌ FAIL'} ({avg_search:.2f}ms at {total_vectors:,} vectors)")
    print("=" * 70)

if __name__ == "__main__":
    benchmark()
