class DailyTaskManager:
    def __init__(self):
        self.checklist = []
        self.completed_tasks = []
        self.incomplete_tasks = []
    
    def add_task(self, task):
        self.checklist.append(task)
        print(f"Task '{task}' added to checklist")
    
    def add_multiple_tasks(self, tasks):
        for task in tasks:
            self.checklist.append(task)
        print(f"{len(tasks)} tasks added to checklist")
    
    def mark_task_completed(self, task):
        if task in self.checklist:
            self.checklist.remove(task)
            self.completed_tasks.append(task)
            print(f"Task '{task}' marked as completed")
        else:
            print(f"Task '{task}' not found in checklist")
    
    def mark_task_incomplete(self, task):
        if task in self.checklist:
            self.checklist.remove(task)
            self.incomplete_tasks.append(task)
            print(f"Task '{task}' marked as incomplete")
        else:
            print(f"Task '{task}' not found in checklist")
    
    def review_remaining_tasks(self):
        if not self.checklist:
            print("No remaining tasks to review!")
            return
        
        print("\n--- Task Review ---")
        for task in self.checklist[:]:  # Create a copy to avoid issues during iteration
            print(f"\nTask: '{task}'")
            while True:
                status = input("Was this task completed? (y/n): ").lower().strip()
                if status in ['y', 'yes']:
                    self.mark_task_completed(task)
                    break
                elif status in ['n', 'no']:
                    self.mark_task_incomplete(task)
                    break
                else:
                    print("Please enter 'y' for yes or 'n' for no")
    
    def bulk_mark_tasks(self, completed_task_names=None, incomplete_task_names=None):
        if completed_task_names:
            for task in completed_task_names:
                self.mark_task_completed(task)
        
        if incomplete_task_names:
            for task in incomplete_task_names:
                self.mark_task_incomplete(task)
    
    def display_summary(self):
        print("\n" + "="*50)
        print("           DAILY TASK SUMMARY")
        print("="*50)
        
        print(f"\n📋 REMAINING TASKS ({len(self.checklist)}):")
        if self.checklist:
            for i, task in enumerate(self.checklist, 1):
                print(f"  {i}. {task}")
        else:
            print("  None")
        
        print(f"\n✅ COMPLETED TASKS ({len(self.completed_tasks)}):")
        if self.completed_tasks:
            for i, task in enumerate(self.completed_tasks, 1):
                print(f"  {i}. {task}")
        else:
            print("  None")
        
        print(f"\n❌ INCOMPLETE TASKS ({len(self.incomplete_tasks)}):")
        if self.incomplete_tasks:
            for i, task in enumerate(self.incomplete_tasks, 1):
                print(f"  {i}. {task}")
        else:
            print("  None")
        
        # Calculate completion rate
        total_processed = len(self.completed_tasks) + len(self.incomplete_tasks)
        if total_processed > 0:
            completion_rate = (len(self.completed_tasks) / total_processed) * 100
            print(f"\n📊 Completion Rate: {completion_rate:.1f}%")
    
    def clear_all(self):
        self.checklist.clear()
        self.completed_tasks.clear()
        self.incomplete_tasks.clear()
        print("All tasks cleared - ready for a new day!")


def demo():
    print("🌅 Starting Daily Task Manager Demo")
    print("-" * 40)
    
    # Create task manager
    tm = DailyTaskManager()
    
    # Add tasks to checklist
    daily_tasks = [
        "Review emails",
        "Complete project report",
        "Call client about meeting",
        "Update website content",
        "Prepare presentation slides",
        "Exercise for 30 minutes",
        "Read industry news",
        "Plan tomorrow's schedule"
    ]
    
    tm.add_multiple_tasks(daily_tasks)
    print(f"\n✨ Started day with {len(daily_tasks)} tasks")
    
    # Simulate end of day - mark some tasks as completed/incomplete
    completed = [
        "Review emails",
        "Complete project report", 
        "Exercise for 30 minutes",
        "Read industry news"
    ]
    
    incomplete = [
        "Call client about meeting",
        "Update website content",
        "Prepare presentation slides"
    ]
    
    print("\n🌆 End of day - reviewing tasks...")
    tm.bulk_mark_tasks(completed, incomplete)
    
    # Display final summary
    tm.display_summary()


def interactive_task_manager():
    tm = DailyTaskManager()
    
    while True:
        print("\n" + "="*40)
        print("     DAILY TASK MANAGER")
        print("="*40)
        print("1. Add task")
        print("2. Add multiple tasks")
        print("3. Mark task as completed")
        print("4. Mark task as incomplete") 
        print("5. Review remaining tasks")
        print("6. Display summary")
        print("7. Clear all tasks")
        print("8. Exit")
        
        choice = input("\nChoose an option (1-8): ").strip()
        
        if choice == '1':
            task = input("Enter task: ").strip()
            if task:
                tm.add_task(task)
        
        elif choice == '2':
            print("Enter tasks one by one (press Enter twice when done):")
            tasks = []
            while True:
                task = input("Task: ").strip()
                if not task:
                    break
                tasks.append(task)
            if tasks:
                tm.add_multiple_tasks(tasks)
        
        elif choice == '3':
            if tm.checklist:
                print("Current tasks:")
                for i, task in enumerate(tm.checklist, 1):
                    print(f"{i}. {task}")
                task = input("Enter task to mark as completed: ").strip()
                tm.mark_task_completed(task)
            else:
                print("No tasks in checklist!")
        
        elif choice == '4':
            if tm.checklist:
                print("Current tasks:")
                for i, task in enumerate(tm.checklist, 1):
                    print(f"{i}. {task}")
                task = input("Enter task to mark as incomplete: ").strip()
                tm.mark_task_incomplete(task)
            else:
                print("No tasks in checklist!")
        
        elif choice == '5':
            tm.review_remaining_tasks()
        
        elif choice == '6':
            tm.display_summary()
        
        elif choice == '7':
            confirm = input("Are you sure you want to clear all tasks? (y/n): ")
            if confirm.lower() in ['y', 'yes']:
                tm.clear_all()
        
        elif choice == '8':
            print("Goodbye! Have a productive day! 🌟")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    print("Choose mode:")
    print("1. Demo mode")
    print("2. Interactive mode")
    mode = input("Enter choice (1 or 2): ").strip()
    if mode == '1':
        demo()
    elif mode == '2':
        interactive_task_manager()
    else:
        print("Invalid choice, running demo mode...")
        demo()

