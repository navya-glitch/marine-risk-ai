#!/usr/bin/env python3
"""
Simple test script to verify the Marine Risk AI backend
Run this after installing dependencies: pip install -r requirements.txt
"""

import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_agents():
    """Test all agents with sample data"""
    
    print("🧪 Testing Marine Risk AI Backend\n")
    
    # Sample input
    test_input = {
        "vessel_name": "MV Neptune Star",
        "imo_number": "IMO9547821",
        "owner": "Neptune Maritime Corp",
        "country_of_registry": "Panama",
        "departure_port": "Rotterdam",
        "destination_port": "Shanghai",
        "cargo_type": "Container"
    }
    
    print("📝 Test Input:")
    for key, value in test_input.items():
        print(f"  {key}: {value}")
    print()
    
    try:
        # Test entity extraction
        print("1️⃣ Testing Entity Extraction...")
        from agents.entity_extractor import run_entity_extraction
        entity_result = await run_entity_extraction(test_input)
        print(f"   ✅ Status: {entity_result['status']}")
        print(f"   📊 Confidence: {entity_result['data']['overall_confidence']:.0%}")
        print()
        
        # Test orchestrator (full workflow)
        print("2️⃣ Testing Full Orchestrator Workflow...")
        from agents.orchestrator import run_risk_assessment
        
        import time
        start_time = time.time()
        result = await run_risk_assessment(test_input)
        execution_time = time.time() - start_time
        
        print(f"   ✅ Success: {result['success']}")
        print(f"   ⏱️ Execution Time: {execution_time:.2f}s")
        print(f"   📊 Risk Score: {result['overall_risk']['score']:.1f}/100")
        print(f"   🎯 Decision: {result['overall_risk']['decision']}")
        print(f"   🔒 Confidence: {result['overall_risk']['confidence']:.0%}")
        print()
        
        # Show category scores
        print("3️⃣ Category Scores:")
        for category, data in result['categories'].items():
            print(f"   {category.capitalize()}: {data['score']}/100")
        print()
        
        # Show timeline
        print("4️⃣ Timeline Summary:")
        for i, event in enumerate(result['timeline'][:5], 1):
            print(f"   {i}. {event['agent']} - {event.get('conclusion', 'Completed')[:60]}...")
        if len(result['timeline']) > 5:
            print(f"   ... and {len(result['timeline']) - 5} more events")
        print()
        
        # Performance check
        if execution_time < 60:
            print(f"✅ Performance: PASSED (<60 seconds)")
        else:
            print(f"⚠️ Performance: SLOW (>{execution_time:.0f} seconds)")
        
        print(f"\n🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_agents())
    sys.exit(0 if success else 1)
