#!/usr/bin/env python3
"""
Test script to verify Timer page bug fixes
"""

import os
import sys
import re

def test_nameerror_fix():
    """Test that NameError with col_timer_display is fixed"""
    print("Testing NameError fix...")
    
    with open("pages/1_Timer.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for col_timer_display references
    if "col_timer_display" in content:
        print("❌ col_timer_display still referenced in code")
        return False
    else:
        print("✅ No col_timer_display references found")
        return True

def test_sound_preview_fix():
    """Test that sound preview autoplay is fixed"""
    print("\nTesting sound preview fix...")
    
    with open("pages/1_Timer.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check that preview button uses play_sound with autoplay=True
    preview_pattern = r'st\.button\("🔊 Preview Sound".*?play_sound\(selected_sound,\s*autoplay=True\)'
    
    if re.search(preview_pattern, content, re.DOTALL):
        print("✅ Preview button uses play_sound with autoplay=True")
        return True
    else:
        print("❌ Preview button doesn't use autoplay=True")
        return False

def test_sound_files_exist():
    """Test that all sound files exist"""
    print("\nTesting sound files exist...")
    
    sound_files = [
        "assets/ringtone/classicBell.mp3",
        "assets/ringtone/digitalBeep.mp3",
        "assets/ringtone/natureSound.mp3",
        "assets/ringtone/softChimes.mp3",
        "assets/ringtone/zenBell.mp3"
    ]
    
    all_exist = True
    for sound_file in sound_files:
        if os.path.exists(sound_file):
            print(f"✅ {sound_file} exists")
        else:
            print(f"❌ {sound_file} NOT FOUND")
            all_exist = False
    
    return all_exist

def test_syntax():
    """Test that file has no syntax errors"""
    print("\nTesting syntax...")
    
    try:
        # Try to compile the file
        import py_compile
        py_compile.compile("pages/1_Timer.py", doraise=True)
        print("✅ No syntax errors")
        return True
    except Exception as e:
        print(f"❌ Syntax error: {e}")
        return False

def test_play_sound_function():
    """Test that play_sound function has autoplay parameter"""
    print("\nTesting play_sound function...")
    
    with open("pages/1_Timer.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check function signature
    if "def play_sound(sound_name, autoplay=False):" in content:
        print("✅ play_sound function has autoplay parameter")
        
        # Check that it uses st.audio with autoplay parameter
        if "st.audio(file_path, autoplay=autoplay)" in content:
            print("✅ Uses st.audio with autoplay parameter")
            return True
        else:
            print("❌ Doesn't use st.audio with autoplay parameter")
            return False
    else:
        print("❌ play_sound function missing autoplay parameter")
        return False

def main():
    print("=" * 60)
    print("TIMER PAGE BUG FIX TEST")
    print("=" * 60)
    
    # Change to correct directory
    os.chdir("c:\\Assignment\\PAUSE")
    
    tests_passed = 0
    tests_total = 5
    
    # Run tests
    if test_nameerror_fix():
        tests_passed += 1
    
    if test_sound_preview_fix():
        tests_passed += 1
    
    if test_sound_files_exist():
        tests_passed += 1
    
    if test_syntax():
        tests_passed += 1
    
    if test_play_sound_function():
        tests_passed += 1
    
    print("\n" + "=" * 60)
    print(f"TEST SUMMARY: {tests_passed}/{tests_total} tests passed")
    
    if tests_passed == tests_total:
        print("\n✅ ALL TIMER PAGE BUG FIXES VERIFIED:")
        print("1. ✅ NameError with col_timer_display - FIXED")
        print("2. ✅ Sound preview autoplay - FIXED")
        print("3. ✅ All sound files exist")
        print("4. ✅ No syntax errors")
        print("5. ✅ play_sound function properly implemented")
        return 0
    else:
        print("\n⚠️  Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())