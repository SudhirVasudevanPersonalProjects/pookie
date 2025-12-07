"""Manual integration test for FAISS vector service"""
import asyncio
from app.services.vector_service import vector_service
from app.services.embedding_service import embedding_service

async def test_integration():
    print("=" * 60)
    print("FAISS Vector Service Integration Test")
    print("=" * 60)

    # Load services
    print("\n1. Loading embedding service...")
    embedding_service.load_model()
    print("   ✓ Embedding service ready")

    print("\n2. Initializing FAISS vector service...")
    await vector_service.initialize()
    print(f"   ✓ Vector service ready ({vector_service.index.total_vectors} vectors loaded)")

    # Test 1: Generate embedding and add to index
    print("\n3. Testing add_something_embedding()...")
    emb1 = embedding_service.generate_embedding("I love hiking in the mountains")
    await vector_service.add_something_embedding(1, emb1)
    print(f"   ✓ Added something_id=1 ({vector_service.index.total_vectors} total vectors)")

    # Test 2: Add another embedding
    print("\n4. Adding second embedding...")
    emb2 = embedding_service.generate_embedding("Pizza is my favorite food")
    await vector_service.add_something_embedding(2, emb2)
    print(f"   ✓ Added something_id=2 ({vector_service.index.total_vectors} total vectors)")

    # Test 3: Search for similar
    print("\n5. Testing search_similar()...")
    results = await vector_service.search_similar(emb1, top_k=2)
    print(f"   ✓ Search results for 'hiking' query:")
    for something_id, score in results:
        print(f"      - something_id={something_id}, similarity={score:.4f}")

    # Verify exact match is top result
    assert results[0][0] == 1, "Top result should be exact match (ID=1)"
    assert results[0][1] > 0.99, f"Exact match similarity should be ~1.0, got {results[0][1]}"
    print("   ✓ Exact match validation passed")

    # Test 4: Search with different query
    print("\n6. Searching with 'food' query...")
    results2 = await vector_service.search_similar(emb2, top_k=2)
    print(f"   ✓ Search results:")
    for something_id, score in results2:
        print(f"      - something_id={something_id}, similarity={score:.4f}")

    assert results2[0][0] == 2, "Top result should be exact match (ID=2)"
    print("   ✓ Second search validation passed")

    # Test 5: Save to Supabase Storage
    print("\n7. Testing save_to_storage()...")
    await vector_service.save_to_storage()
    print("   ✓ Saved to Supabase Storage bucket: vector-indices")
    print("      Files: somethings_index.faiss, somethings_index.faiss.ids")

    # Test 6: Reload from storage (simulate restart)
    print("\n8. Testing reload from storage (simulating restart)...")
    from app.ml.vector_index import VectorIndex
    vector_service.index = VectorIndex(dimension=384)  # Reset
    print(f"   - Index reset (vectors: {vector_service.index.total_vectors})")

    await vector_service.initialize()
    print(f"   ✓ Reloaded from storage ({vector_service.index.total_vectors} vectors)")

    # Verify data persisted
    assert vector_service.index.total_vectors == 2, "Should have 2 vectors after reload"
    assert vector_service.index.something_ids == [1, 2], "IDs should match"

    # Verify search still works
    results3 = await vector_service.search_similar(emb1, top_k=1)
    assert results3[0][0] == 1, "Search should still work after reload"
    print("   ✓ Persistence validation passed")

    print("\n" + "=" * 60)
    print("✅ ALL INTEGRATION TESTS PASSED")
    print("=" * 60)
    print(f"\nFinal state:")
    print(f"  - Total vectors in index: {vector_service.index.total_vectors}")
    print(f"  - Something IDs: {vector_service.index.something_ids}")
    print(f"  - Bucket: vector-indices (Supabase Storage)")
    print()

if __name__ == "__main__":
    asyncio.run(test_integration())
