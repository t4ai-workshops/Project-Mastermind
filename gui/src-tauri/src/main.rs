#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use tauri::{Manager, Runtime};
use window_vibrancy::{apply_vibrancy, NSVisualEffectMaterial};

// This command is specific to macOS
#[tauri::command]
fn toggle_fullscreen<R: Runtime>(window: tauri::Window<R>) {
    if let Some(ns_window) = window.ns_window() {
        unsafe {
            ns_window.toggleFullScreen_(None);
        }
    }
}

// This command handles the window titlebar on macOS
#[tauri::command]
fn toggle_titlebar<R: Runtime>(window: tauri::Window<R>, show: bool) {
    if let Some(ns_window) = window.ns_window() {
        unsafe {
            if show {
                ns_window.setTitlebarAppearsTransparent_(cocoa::base::YES);
                ns_window.setTitleVisibility_(cocoa::appkit::NSWindowTitleVisibility::NSWindowTitleVisible);
            } else {
                ns_window.setTitlebarAppearsTransparent_(cocoa::base::YES);
                ns_window.setTitleVisibility_(cocoa::appkit::NSWindowTitleVisibility::NSWindowTitleHidden);
            }
        }
    }
}

fn main() {
    let context = tauri::generate_context!();
    tauri::Builder::default()
        .setup(|app| {
            let window = app.get_window("main").unwrap();
            
            #[cfg(target_os = "macos")]
            {
                // Add vibrancy effect for macOS
                apply_vibrancy(&window, NSVisualEffectMaterial::HudWindow, None, None)
                    .expect("Failed to add vibrancy effect");

                // Configure window for macOS
                if let Some(ns_window) = window.ns_window() {
                    unsafe {
                        use cocoa::appkit::{NSWindow, NSWindowStyleMask};
                        ns_window.setTitlebarAppearsTransparent_(cocoa::base::YES);
                        let style_mask = ns_window.styleMask();
                        ns_window.setStyleMask_(
                            style_mask | NSWindowStyleMask::NSFullSizeContentViewWindowMask
                        );
                        // Enable window to remember size and position
                        ns_window.setRestorable_(cocoa::base::YES);
                    }
                }
            }

            // Enable devtools in debug mode
            #[cfg(debug_assertions)]
            window.open_devtools();

            Ok(())
        })
        .invoke_handler(tauri::generate_handler![toggle_fullscreen, toggle_titlebar])
        .run(context)
        .expect("error while running tauri application");
}