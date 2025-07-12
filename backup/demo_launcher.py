import sys
import os

def display_main_menu():
    print("\n" + "="*70)
    print("🚗 RUSH HOUR PUZZLE SOLVER - DEMO LAUNCHER 🚗")
    print("="*70)
    print("Choose your demo experience:")
    print()
    print("1. 🖼️  GUI Demo (Graphical Interface)")
    print("   - Visual puzzle board")
    print("   - Interactive buttons")
    print("   - Solution animation")
    print("   - Real-time algorithm comparison")
    print()
    print("2. 🎮 Interactive Console Demo")
    print("   - Enhanced text-based interface")
    print("   - Manual puzzle solving mode")
    print("   - Step-by-step solution animation")
    print("   - Algorithm performance comparison")
    print()
    print("3. 📊 Original Console Demo")
    print("   - Simple text output")
    print("   - Algorithm testing")
    print("   - Basic move testing")
    print()
    print("0. Exit")
    print("-"*70)

def run_gui_demo():
    try:
        print("\n🖼️  Starting GUI Demo...")
        print("Note: A pygame window will open. Close the window to return here.")
        
        from gui_demo_rushhour import main as gui_main
        gui_main()
        
    except ImportError as e:
        print(f"❌ Error importing GUI demo: {e}")
        print("Make sure pygame is installed: pip install pygame")
    except Exception as e:
        print(f"❌ Error running GUI demo: {e}")

def run_interactive_demo():
    try:
        print("\n🎮 Starting Interactive Console Demo...")
        
        from interactive_demo_rushhour import main as interactive_main
        interactive_main()
        
    except Exception as e:
        print(f"❌ Error running interactive demo: {e}")

def run_original_demo():
    try:
        print("\n📊 Starting Original Console Demo...")
        
        from demo_rushhour import main as original_main
        original_main()
        
    except Exception as e:
        print(f"❌ Error running original demo: {e}")

def check_dependencies():
    missing_deps = []
    
    # Check pygame for GUI demo
    try:
        import pygame
        pygame_available = True
    except ImportError:
        pygame_available = False
        missing_deps.append("pygame (for GUI demo)")
    
    if missing_deps:
        print("\n⚠️  Missing dependencies:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\nTo install missing dependencies:")
        if "pygame" in str(missing_deps):
            print("   pip install pygame")
        print()
    
    return len(missing_deps) == 0, pygame_available

def main():
    """Main launcher function"""
    print("🚗 Welcome to Rush Hour Puzzle Solver!")
    
    # Check dependencies
    all_deps, pygame_available = check_dependencies()
    
    while True:
        display_main_menu()
        
        if not pygame_available:
            print("ℹ️  Note: GUI demo unavailable (pygame not installed)")
        
        try:
            choice = input("Enter your choice (0-3): ").strip()
            
            if choice == '0':
                print("\n👋 Thanks for using Rush Hour Puzzle Solver! Goodbye!")
                break
                
            elif choice == '1':
                if pygame_available:
                    run_gui_demo()
                else:
                    print("❌ GUI demo requires pygame. Please install it first: pip install pygame")
                    
            elif choice == '2':
                run_interactive_demo()
                
            elif choice == '3':
                run_original_demo()
                
            else:
                print("❌ Invalid choice! Please select 0-3.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            
        if choice in ['1', '2', '3']:
            input("\nPress Enter to return to main menu...")

if __name__ == "__main__":
    # Add current directory to path so imports work
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    main()
