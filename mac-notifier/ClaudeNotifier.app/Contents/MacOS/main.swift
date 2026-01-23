import Cocoa
import UserNotifications

class AppDelegate: NSObject, NSApplicationDelegate, UNUserNotificationCenterDelegate {
    func applicationDidFinishLaunching(_ notification: Notification) {
        // Check if launched from notification click (no command line args means reactivation)
        // When user clicks notification, macOS may relaunch app without our custom args
        let args = CommandLine.arguments
        let hasMessageArg = args.contains("-message") || args.contains("-m")

        if !hasMessageArg {
            // Launched from notification click or without args, just exit
            NSApp.terminate(nil)
            return
        }

        let center = UNUserNotificationCenter.current()
        center.delegate = self

        center.requestAuthorization(options: [.alert, .sound]) { granted, error in
            if granted {
                self.sendNotification()
            } else {
                // Fallback to osascript
                self.sendNotificationViaAppleScript()
            }
            // Give notification time to be delivered before exiting
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
                NSApp.terminate(nil)
            }
        }
    }

    // Handle notification click - just exit without sending new notification
    func userNotificationCenter(_ center: UNUserNotificationCenter, didReceive response: UNNotificationResponse, withCompletionHandler completionHandler: @escaping () -> Void) {
        completionHandler()
        NSApp.terminate(nil)
    }

    func sendNotification() {
        let args = CommandLine.arguments
        var title = "Claude Code"
        var message = "Notification"
        var subtitle = ""
        var sound = "Glass"

        var i = 1
        while i < args.count {
            switch args[i] {
            case "-title": title = args[i + 1]; i += 2
            case "-message": message = args[i + 1]; i += 2
            case "-subtitle": subtitle = args[i + 1]; i += 2
            case "-sound": sound = args[i + 1]; i += 2
            default: i += 1
            }
        }

        let content = UNMutableNotificationContent()
        content.title = title
        content.body = message
        if !subtitle.isEmpty { content.subtitle = subtitle }
        content.sound = UNNotificationSound(named: UNNotificationSoundName(rawValue: sound))

        let request = UNNotificationRequest(identifier: UUID().uuidString, content: content, trigger: nil)
        UNUserNotificationCenter.current().add(request)
    }

    func sendNotificationViaAppleScript() {
        let args = CommandLine.arguments
        var title = "Claude Code"
        var message = "Notification"
        var sound = "Glass"

        var i = 1
        while i < args.count {
            switch args[i] {
            case "-title": title = args[i + 1]; i += 2
            case "-message": message = args[i + 1]; i += 2
            case "-sound": sound = args[i + 1]; i += 2
            default: i += 1
            }
        }

        let script = "display notification \"\(message)\" with title \"\(title)\" sound name \"\(sound)\""
        if let appleScript = NSAppleScript(source: script) {
            appleScript.executeAndReturnError(nil)
        }
    }

    func userNotificationCenter(_ center: UNUserNotificationCenter, willPresent notification: UNNotification, withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void) {
        completionHandler([.banner, .sound])
    }
}

let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate
app.run()
