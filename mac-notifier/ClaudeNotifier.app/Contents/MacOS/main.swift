import Cocoa
import UserNotifications

class AppDelegate: NSObject, NSApplicationDelegate, UNUserNotificationCenterDelegate {
    func applicationDidFinishLaunching(_ notification: Notification) {
        let center = UNUserNotificationCenter.current()
        center.delegate = self

        center.requestAuthorization(options: [.alert, .sound]) { granted, error in
            if granted {
                self.sendNotification()
            } else {
                // Fallback to osascript
                self.sendNotificationViaAppleScript()
            }
            DispatchQueue.main.async {
                NSApp.terminate(nil)
            }
        }
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
