#!/usr/bin/env python3
"""
Enhancement Status Checker
Shows which scripts have been enhanced and which need work
"""

import os
from pathlib import Path

def check_status():
    """Check enhancement status of all Python files"""
    
    print("="*80)
    print("📋 QUANTUM SCRIPT ENHANCEMENT STATUS".center(80))
    print("="*80)
    
    enhanced = []
    needs_work = []
    
    # Get all Python files
    for file in sorted(Path('.').glob('*.py')):
        if file.name == 'check_enhancement_status.py':
            continue
            
        try:
            with open(file, 'r') as f:
                content = f.read()
                
            if 'ENHANCED' in content or 'Enhanced' in content:
                enhanced.append(file.name)
            else:
                needs_work.append(file.name)
        except:
            needs_work.append(file.name)
    
    # Show enhanced scripts
    print(f"\n✅ ENHANCED SCRIPTS ({len(enhanced)}):")
    print("-"*80)
    for script in enhanced:
        print(f"  ✨ {script}")
    
    # Show scripts needing work
    print(f"\n⚠️  SCRIPTS NEEDING ENHANCEMENT ({len(needs_work)}):")
    print("-"*80)
    for i, script in enumerate(needs_work[:10], 1):
        marker = "👉" if i == 1 else "  "
        print(f"  {marker} {script}")
    
    if len(needs_work) > 10:
        print(f"  ... and {len(needs_work) - 10} more")
    
    # Statistics
    total = len(enhanced) + len(needs_work)
    percent = (len(enhanced) / total * 100) if total > 0 else 0
    
    print("\n" + "="*80)
    print("📊 STATISTICS".center(80))
    print("="*80)
    print(f"  Total Scripts: {total}")
    print(f"  Enhanced: {len(enhanced)} ({percent:.1f}%)")
    print(f"  Remaining: {len(needs_work)}")
    print("="*80)
    
    # Next to enhance
    if needs_work:
        print(f"\n🎯 NEXT TO ENHANCE: {needs_work[0]}")
    else:
        print("\n🎉 ALL SCRIPTS ENHANCED!")
    
    print()

if __name__ == "__main__":
    check_status()
