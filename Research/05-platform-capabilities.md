# Hydrate: Platform Capabilities, HealthKit, Liquid Glass, Widgets and Data Layer (iOS 27.2 / Xcode 27, free Personal Team)

Research date: 2026-11-13. Sources accessed that day. Apple doc pages were read through their markdown endpoints (`developer.apple.com/documentation/<path>.md`), which include each symbol's availability metadata. Every API marked **unverified** is one I could not confirm in Apple's documentation index.

---

## TL;DR

### Capability matrix (free Apple ID "Personal Team", iOS)

| Capability | Free team? | Notes | Source |
|---|---|---|---|
| **HealthKit** | **Yes** | Listed for the free "Apple Developer" tier. It needs an explicit App ID, so every person who builds the open-source project needs their own bundle ID. | [1] (Apple, page © 2026, read 2026-11-13); [3] (Apple DTS, June 2026) |
| HealthKit **Background Delivery** sub-entitlement | **Unknown** | `com.apple.developer.healthkit.background-delivery` has been required since iOS 15 [11]. The capability table doesn't list it separately, and I found no free-team report. Test it, and design so the app doesn't depend on it. | [1], [11] |
| **App Groups** (app ↔ widget/control data sharing) | **Yes** | Ticked for the free tier in [1]. DTS confirmed in June 2026 that personal teams can use it with per-developer group IDs [3]. A third-party tool's notes (Oct 2026, iOS 27.2) say free teams get **one group per app** [5]. Some older community reports say free-team profiles came with an empty group list, so verify on your own build. | [1], [3], [5] |
| **WidgetKit widgets** (Home Screen, Lock Screen, StandBy) | **Yes** | No entitlement needed. Each widget extension is its own App ID and counts against the 10-App-ID/7-day limit [2]. Sharing data with the app needs App Groups. | [1], [2], [38] |
| **Control Center controls** (`ControlWidget`) | **Yes** | Lives in a widget extension. No extra entitlement. | [39], [40] |
| **App Intents / App Shortcuts / Shortcuts app / Spotlight / Action button** | **Yes (likely)** | App Intents doesn't use the SiriKit "Siri" capability. Apple's App Shortcuts docs mention no entitlement [43]. | [43], [52] |
| **Siri voice phrases for App Shortcuts** | **Partial / verify** | The **Siri capability is not available** to free teams [1], but that capability is for SiriKit (`INIntent`). One unverified developer report says Siri voice invocation failed without it [77]. Test on device. | [1], [77] |
| **Siri AI tool intents** (`@AppIntent(.tool)`, iOS 27.3 beta) | **Maybe** | Developer preview from 2026-11-03. Reportedly needs no new entitlement or program, and runs on development-signed builds [51]. It needs iOS 27.3 (beta) and an Apple Intelligence device. Can't ship to the App Store until spring 2027 (not relevant to Hydrate). | [50], [51] |
| **iCloud** (CloudKit, iCloud Documents, KVS) | **No** | Not ticked for the free tier. So **no SwiftData + CloudKit sync and no `NSUbiquitousKeyValueStore`.** | [1] |
| **Push notifications** (APNs) | **No** | Not ticked [1]. Local notifications need no capability. | [1] |
| **Time Sensitive notifications** | **No** | Not ticked [1]. Use normal (active) interruption level. | [1] |
| **Local notifications** (`UNUserNotificationCenter`) | **Yes** | No entitlement. You just ask the user for permission at runtime. | [72] |
| **Background Modes** (e.g. BGAppRefreshTask) | **Yes** | Ticked [1]. The system decides timing, and nothing is guaranteed. | [1] |
| **Keychain Sharing** | **Yes** | Ticked [1]. Fine for tiny shared values, not a store. | [1] |
| **Data Protection** | **Yes** | Ticked [1]. | [1] |
| **Associated Domains, Sign in with Apple, WeatherKit, In-App Purchase, Game Center** | **No** | Not needed by Hydrate. | [1] |
| **Live Activities** | n/a | The user doesn't want them. (WWDC26 `LongRunningIntent` shows progress as a Live Activity, so avoid it [47].) | — |
| **Alternate app icons** (`setAlternateIconName`) | **Yes** | No entitlement. Apple's current sample uses Icon Composer `.icon` files [68]. | [67], [68] |

**Free-team limits (Apple, "Choosing a membership" [2]):** up to **10 App IDs**, each expiring after **7 days**. Up to **3 registered devices**, which also expire after 7 days. Up to **3 apps per device**. Provisioning profiles expire **7 days after issue**, so you must rebuild and reinstall from Xcode at least weekly. Apple DTS has said these limits aren't well documented, and suggests reusing bundle IDs [4]. **The free tier can't distribute apps at all [1][2].** Friends have to build Hydrate themselves from the open-source repo with their own Apple ID, or plug their phone into your Mac, which uses up your 3-device slots.

### Key takeaways

1. **Everything Hydrate needs works on a free team: HealthKit, App Groups, widgets, controls, App Intents, local notifications and background modes.** iCloud/CloudKit, push, Time Sensitive notifications and the SiriKit "Siri" capability don't.
2. **Open-source setup:** entitled App IDs (HealthKit, App Groups) belong to one team, and personal teams can't share them [3]. Put `DEVELOPMENT_TEAM`, `PRODUCT_BUNDLE_IDENTIFIER` and the App Group ID in a git-ignored `.xcconfig` (with a template checked in). Read the group ID at runtime from an Info.plist key that the build setting fills in.
3. **Backup/sync without iCloud:** SwiftData store in the App Group container (included in normal device backups), plus manual JSON/CSV export and import through the Files app. Saving to iCloud Drive from the system file exporter needs **no** iCloud entitlement. HealthKit gives a second, Apple-synced copy of water totals.
4. **HealthKit:** one-way push from the SwiftData source of truth, with `HKMetadataKeySyncIdentifier`/`SyncVersion` so edits replace and deletes stay idempotent [6][7]. Optional read-only import of *other apps'* water through an anchored query that excludes our own source.
5. **Liquid Glass:** iOS 27 adds `Tab(role: .prominent)` [16] (a set-apart trailing tab, better than misusing `.search`). The HIG says tab bars are for navigation, not actions [33]. Recommended pattern: a prominent glass "+" that presents a sheet, done either with an intercepted tab selection or with `tabViewBottomAccessory`.
6. **Widgets and intents:** one `LogDrinkIntent` reused by interactive widgets, a Control Center control, App Shortcuts and (optionally) a Siri AI tool. Intents that run in the widget process write to the shared SwiftData store. HealthKit writes go through an "outbox" that the app drains, or run in the app process (`supportedModes` [45] / iOS 27 `allowedExecutionTargets` [46]).
7. **Watch for these:** `fileExporter(…document: FileDocument…)` is marked deprecated in the iOS 27.3 SDK [64], so use the `Transferable` `item:` variant [65]. `toolbarMinimizeBehavior` was shown at WWDC26 [29] but isn't in the docs index (**unverified**).

---

## 1. Free Personal Team capabilities (highest priority)

### 1.1 What the authoritative table says

Apple's **Supported capabilities (iOS)** page [1] has three columns: ADP (paid), ADEP (enterprise) and **Apple Developer**, which it defines as a free Apple Account that accepted the Developer Agreement and can't distribute apps. I parsed the raw HTML table on 2026-11-13. The **free column has a tick for only these:** App Groups, Background Modes, Data Protection, **HealthKit**, HomeKit, Inter-App Audio, Keychain Sharing, Maps (no routing), Wireless Accessory Configuration.

Everything else is paid-only, including **iCloud (CloudKit / Documents / KVS)**, **Push Notifications**, **Siri**, **Time Sensitive Notifications**, Associated Domains, App Attest, Sign in with Apple, WeatherKit, Communication Notifications and Increased Debugging Memory Limit.

The page carries only a 2026 copyright and no "last updated" date. Treat it as current as of the access date.

### 1.2 Per-item verdicts for Hydrate

| Need | Verdict | Detail |
|---|---|---|
| HealthKit read/write | **Yes** [1] | A DTS thread (June 2026) about personal teams with HealthKit + App Groups + widget confirms it works per developer. It also confirms an entitled explicit App ID can't be reused across personal teams [3]. |
| HealthKit background delivery | **Unknown** | The entitlement has been mandatory since iOS 15. Without it, `enableBackgroundDelivery` fails with an authorization-denied error [11]. Plan for foreground refresh (on `scenePhase == .active`) as the baseline. |
| App Groups | **Yes** [1][3] | Expect one group per app on a free team [5] (third-party, Oct 2026). Older community reports of empty `application-groups` in free profiles mostly involve sideloading tools. The DTS reply and the table both say Xcode-managed signing supports it. **Do a 10-minute smoke test first:** app + widget, both with the group, write in the app, read in the widget. |
| WidgetKit | **Yes** | No capability. The widget extension needs its own App ID (`<app id>.Widgets`), which counts toward the 10-per-7-days limit [2]. |
| App Intents / Shortcuts | **Yes** | No entitlement in Apple's docs [43]. |
| Siri voice | **Verify** | The Siri capability isn't available [1]. That's SiriKit's entitlement (`com.apple.developer.siri`) for Intents extensions, which Hydrate doesn't need. App Shortcuts phrases are expected to work, but there's one contrary unverified report [77]. |
| Push vs local notifications | **Local only** | Push and Time Sensitive need a paid team [1]. Local scheduled reminders work. |
| Background tasks | **Yes** [1] | `BGAppRefreshTask` for rescheduling reminders and refreshing widgets. Best-effort timing. |
| iCloud / CloudKit | **No** [1] | See 1.4. |

### 1.3 Free-team operational limits

From Apple's "Choosing a membership" page [2]:
- **10 App IDs**, which expire after 7 days. App + widget extension = 2. Keep bundle IDs stable while you experiment, because each new one uses a slot [4].
- **3 devices**, which expire after 7 days.
- **3 apps per device**, and **profiles expire 7 days after issue**. After that the app won't launch until you rebuild and reinstall from Xcode. Its data stays in place as long as the bundle ID and team don't change and you don't delete the app.
- No TestFlight and no App Store Connect. Distribution means "friends build from source."

**Practical advice**
- Add a "Last installed / expires" hint in Settings (build date + 7 days) so you remember to re-run from Xcode.
- Put the app and every extension's bundle ID under one prefix, set from `.xcconfig`:

```xcconfig
// Config/Local.xcconfig  (git-ignored; copy from Local.xcconfig.template)
DEVELOPMENT_TEAM = ABCDE12345
HYDRATE_BUNDLE_PREFIX = com.yourname.hydrate
PRODUCT_BUNDLE_IDENTIFIER = $(HYDRATE_BUNDLE_PREFIX)
HYDRATE_APP_GROUP = group.$(HYDRATE_BUNDLE_PREFIX)
```

Reference `$(HYDRATE_APP_GROUP)` in both targets' `.entitlements` (`com.apple.security.application-groups`). Expose it to code through an Info.plist key, e.g. `HydrateAppGroup = $(HYDRATE_APP_GROUP)`, read with `Bundle.main.object(forInfoDictionaryKey:)`.

### 1.4 No iCloud: backup and sync alternatives

| Option | Works on free team? | Notes |
|---|---|---|
| **Local SwiftData store in the App Group container** | Yes | Survives app updates and re-signing (same bundle ID/team). It's included in the device's iCloud/Finder backup like any app container. Lost if the app is deleted or the bundle ID changes. |
| **Manual export → Files app (JSON + CSV)** | Yes | `fileExporter(isPresented:item:contentTypes:…)` with a `Transferable` payload (iOS 17+) [65]. The **FileDocument-based `fileExporter(…document:contentType:…)` shows availability "iOS 14.0 – 27.3"** in Apple's docs, i.e. deprecated in the 27.3 SDK [64], so don't build on it. The user can choose **iCloud Drive** in the picker; that runs out-of-process and needs **no** iCloud entitlement. |
| **Import ← Files** | Yes | `fileImporter(isPresented:allowedContentTypes:allowsMultipleSelection:onCompletion:)` [66]. Call `startAccessingSecurityScopedResource()` on the returned URL. |
| **ShareLink** of the export | Yes | Lets users AirDrop or Mail the backup to another device. |
| **HealthKit as an implicit backup** | Yes | Water/caffeine samples you write are synced by Apple Health itself. Hydrate's own samples, with sync identifiers and custom metadata (drink type, original volume), can be re-imported after a reinstall. This only works if the bundle ID (HKSource) is the same, or if you match on metadata instead of source. |
| SwiftData + CloudKit | **No** | Needs the iCloud capability [1]. |
| `NSUbiquitousKeyValueStore` | **No** | Needs the iCloud KVS capability [1]. |

**Is "local SwiftData + export" enough?** Yes, for a personal or friends app. Add:
1. a versioned JSON format (`{"format":"hydrate-backup","version":1,"exportedAt":…,"profile":…,"drinks":[…]}`) that import is idempotent against, by deduplicating on drink `id`;
2. a CSV export for spreadsheets;
3. an optional "auto-export weekly" reminder, a local notification that deep-links to the export screen. A fully automatic background write to a user-chosen folder would need a security-scoped bookmark, and it's brittle.

```swift
import CoreTransferable
import UniformTypeIdentifiers

struct HydrateBackup: Codable, Transferable {
    var format = "hydrate-backup"
    var version = 1
    var exportedAt = Date()
    var drinks: [DrinkDTO]
    var profileHistory: [ProfileSnapshotDTO]

    static var transferRepresentation: some TransferRepresentation {
        CodableRepresentation(contentType: .json)
    }
}

// In a Settings view
.fileExporter(isPresented: $isExporting,
              item: backup,
              contentTypes: [.json],
              defaultFilename: "Hydrate-\(Date.now.formatted(.iso8601.year().month().day()))") { result in
    // handle Result<URL, Error>
}
.fileImporter(isPresented: $isImporting, allowedContentTypes: [.json]) { result in
    guard case .success(let url) = result, url.startAccessingSecurityScopedResource() else { return }
    defer { url.stopAccessingSecurityScopedResource() }
    // decode + merge by id
}
```
(I verified the `item:contentTypes:` overload's existence and iOS 17 availability [65]. Check the exact parameter list in Xcode.)

---

## 2. HealthKit for water

### 2.1 Types

| Purpose | Identifier | Unit | Notes |
|---|---|---|---|
| Water | `HKQuantityTypeIdentifier.dietaryWater` | volume (`.literUnit(with: .milli)`) | Cumulative aggregation [8]. |
| Caffeine | `.dietaryCaffeine` | `.gramUnit(with: .milli)` | iOS 8+. |
| Sugar | `.dietarySugar` | `.gram()` | iOS 8+. |
| Energy (optional, for sugary drinks) | `.dietaryEnergyConsumed` | `.kilocalorie()` | Write it only if Hydrate actually knows the kcal. Otherwise skip, since HealthKit is the user's nutrition record. |
| Group a drink's nutrients (optional) | `HKCorrelationTypeIdentifier.food` | — | A food correlation bundles water + caffeine + sugar for one drink. Adds complexity: correlations aren't eligible for background delivery [11]. Recommend **not** using correlations in v1. Use shared metadata instead (same sync-identifier prefix, plus `HKMetadataKeyFoodType` = drink name). |
| Read: weight | `.bodyMass` | kg | Goal calculation. |
| Read: height | `.height` | m | Optional. |
| Read: DOB, sex | characteristics: `dateOfBirthComponents()`, `biologicalSex()` | — | Synchronous characteristic reads. They throw or return "not set" if the user denied access or didn't set them. |
| Read: activity | `.activeEnergyBurned`, `.stepCount` | kcal, count | Activity-based goal bump. Use `HKStatisticsCollectionQueryDescriptor` for daily sums. |

**What to write as "water":** Apple Health's Water is water consumed. Recommendation: write **effective water** (volume × the drink's water fraction, e.g. coffee ~0.98, milk ~0.88) as `dietaryWater`. Store the original volume and drink type in custom metadata (string/number keys of your own, e.g. `"HydrateDrinkType"`, `"HydrateVolumeML"`). Write caffeine and sugar as separate samples that share the same timestamp. Document the choice in the app's About screen.

### 2.2 Authorization model

- Request with the SwiftUI modifier `healthDataAccessRequest(store:shareTypes:readTypes:trigger:completion:)` (iOS 17+) [14] or `requestAuthorization(toShare:read:)`.
- **Read denial is invisible.** `authorizationStatus(for:)` reports **share** (write) status only. If read access is denied, it just looks as if there's no data. With write-but-not-read access you see only your own samples [9][10]. UI copy should say "No weight found in Health. Enter it manually," not "Permission denied."
- Use `getRequestStatusForAuthorization(toShare:read:completion:)` to decide whether to show the "Connect Health" button. It says whether the sheet *would* be shown, not what the user picked.
- Info.plist needs `NSHealthShareUsageDescription` and `NSHealthUpdateUsageDescription`, or the app crashes when it requests access [10].
- **The HealthKit store is encrypted while the device is locked.** Reads can fail in the background. Writes are cached and committed after unlock [10].
- **Extensions can't prompt.** A widget calling requestAuthorization gets an error (forum, error 111) [15]. Always request in the app, during onboarding.

### 2.3 Writing with sync identifiers (edits and deletes)

When you save an object whose `HKMetadataKeySyncIdentifier` matches an existing one, HealthKit compares `HKMetadataKeySyncVersion` and replaces the old object if the new version is higher. Both keys are required together [6][7].

```swift
import HealthKit

let store = HKHealthStore()
let ml = HKUnit.literUnit(with: .milli)

func healthSamples(for log: DrinkLog) -> [HKQuantitySample] {
    var out: [HKQuantitySample] = []
    let baseMeta: [String: Any] = [
        HKMetadataKeySyncVersion: log.syncVersion,          // NSNumber/Int, bump on every edit
        HKMetadataKeyWasUserEntered: true,
        HKMetadataKeyFoodType: log.drinkName,
        "HydrateDrinkType": log.drinkTypeRaw,
        "HydrateVolumeML": log.volumeML
    ]
    func meta(_ suffix: String) -> [String: Any] {
        baseMeta.merging([HKMetadataKeySyncIdentifier: "\(log.id.uuidString).\(suffix)"]) { $1 }
    }
    out.append(HKQuantitySample(type: HKQuantityType(.dietaryWater),
                                quantity: HKQuantity(unit: ml, doubleValue: log.effectiveWaterML),
                                start: log.timestamp, end: log.timestamp, metadata: meta("water")))
    if let mg = log.caffeineMG, mg > 0 {
        out.append(HKQuantitySample(type: HKQuantityType(.dietaryCaffeine),
                                    quantity: HKQuantity(unit: .gramUnit(with: .milli), doubleValue: mg),
                                    start: log.timestamp, end: log.timestamp, metadata: meta("caffeine")))
    }
    if let g = log.sugarG, g > 0 {
        out.append(HKQuantitySample(type: HKQuantityType(.dietarySugar),
                                    quantity: HKQuantity(unit: .gram(), doubleValue: g),
                                    start: log.timestamp, end: log.timestamp, metadata: meta("sugar")))
    }
    return out
}

// Create or edit: bump syncVersion, then save. HealthKit replaces lower versions.
try await store.save(healthSamples(for: log))
```

**Deleting our own samples** (apps can delete only objects they saved) [13]:

```swift
func deleteFromHealth(_ id: UUID) async throws {
    let ids = ["water", "caffeine", "sugar"].map { "\(id.uuidString).\($0)" }
    let byID = HKQuery.predicateForObjects(withMetadataKey: HKMetadataKeySyncIdentifier, allowedValues: ids)
    let mine = HKQuery.predicateForObjects(from: HKSource.default())
    let pred = NSCompoundPredicate(andPredicateWithSubpredicates: [byID, mine])
    for t in [HKQuantityType(.dietaryWater), HKQuantityType(.dietaryCaffeine), HKQuantityType(.dietarySugar)] {
        _ = try await store.deleteObjects(of: t, predicate: pred)   // async overload of deleteObjects(of:predicate:withCompletion:)
    }
}
```
If an edit drops caffeine to 0, delete the `.caffeine` sample rather than writing 0.

### 2.4 Observer, background delivery and anchored queries

- `HKObserverQuery` tells you that something changed. `enableBackgroundDelivery(for:frequency:)` wakes the app at most once per period, but needs the background-delivery entitlement, whose free-team status is **unknown** [11].
- `HKAnchoredObjectQueryDescriptor` (iOS 15.4+) [12] returns added samples, deleted objects and a new anchor. Persist the anchor (e.g. `NSKeyedArchiver` → `Data` in SwiftData or UserDefaults in the group) for an incremental "sync history." `results(for:)` gives a long-running async sequence while the app is in the foreground.

```swift
// Import water logged by OTHER apps (read-only), excluding our own source to avoid echo.
let notMine = NSCompoundPredicate(notPredicateWithSubpredicate:
                 HKQuery.predicateForObjects(from: HKSource.default()))
let descriptor = HKAnchoredObjectQueryDescriptor(
    predicates: [.quantitySample(type: HKQuantityType(.dietaryWater), predicate: notMine)],
    anchor: savedAnchor)
let result = try await descriptor.result(for: store)
// result.addedSamples, result.deletedObjects, result.newAnchor → upsert/delete ExternalWaterSample rows keyed by sample.uuid
```
(Result property names are as I recall them from Apple's docs. Confirm with autocomplete.)

### 2.5 Should Hydrate import other apps' water?

Yes, **as an opt-in, read-only mirror**. Show it as "From Health: 500 ml (Apple Watch / WaterMinder …)" in the day total, keep it in a separate `ExternalWaterSample` model keyed by HealthKit UUID, and never re-write it to HealthKit. Hydrate can't edit or delete other apps' samples [13], so those rows are view-only. Let the user exclude specific sources (a total that counts both Hydrate and a second tracker would double-count).

### 2.6 Recommended sync architecture

**SwiftData is the source of truth. One-way push to HealthKit, plus an optional one-way pull of foreign water.**

```
 UI / Widget intent / Control / Siri
            │  (write DrinkLog, healthState = .pending, syncVersion += 1)
            ▼
     SwiftData (App Group)  ──outbox──▶  HealthSyncService (app process)
            ▲                               │ save()/deleteObjects() with SyncIdentifier
            │                               ▼
  ExternalWaterSample ◀── anchored query ── HealthKit (other sources only)
```

- **Why not two-way?** Two-way would mean reconciling HealthKit edits back into Hydrate's model. HealthKit has no "edit" for foreign samples, users rarely edit water in the Health app, and the echo and loop risks aren't worth it. Sync identifiers already make the push idempotent.
- **Outbox fields on DrinkLog:** `healthState` (`pending`, `synced`, `pendingDelete`, `failed`), `syncVersion`. Deletes become a soft delete (`deletedAt`) until the HealthKit delete succeeds, then the row is purged.
- **When to drain:** on app foreground, after each in-app log, and in a `BGAppRefreshTask`. Widget and Control intents running in the extension only write SwiftData. The app drains the outbox next time it runs, or the intent runs in the app process (see §4.5).

---

## 3. Liquid Glass UI APIs (iOS 26 → 27)

Availability shown is from Apple's doc metadata.

### 3.1 TabView: search tab, prominent tab, intercepting selection

- `TabRole.search` (iOS 18+). On iOS 26+ it renders as a separate circular button at the trailing end [28][33].
- **`TabRole.prominent` is new in iOS 27** [16]. Only one tab gets it. If none is marked, a `.search` tab may get the prominent treatment by default. WWDC26 demoed it for a "Cart" tab [29].
- `tabViewSearchActivation(_:)` / `TabSearchActivation.searchTabSelection` (iOS 26) ties search-field activation to tab selection [32]. Only relevant if the tab really is search.
- **HIG:** "Use a tab bar to support navigation, not to provide actions" [33]. A "+" tab that opens a sheet goes against this, so it's a deliberate trade-off. The HIG-friendly alternatives are a `tabViewBottomAccessory` quick-add bar, or a glass "+" toolbar button.

**Intercepting selection to present a sheet** (works with `.prominent` or `.search`. Whether a `.search` tab without `.searchable` behaves like a plain button is **unverified**, so prefer `.prominent` on iOS 27):

```swift
enum AppTab: Hashable { case today, history, insights, add }

struct RootView: View {
    @State private var selection: AppTab = .today
    @State private var showAddSheet = false

    private var tabSelection: Binding<AppTab> {
        Binding(get: { selection },
                set: { newValue in
                    if newValue == .add { showAddSheet = true }   // don't switch tabs
                    else { selection = newValue }
                })
    }

    var body: some View {
        TabView(selection: tabSelection) {
            Tab("Today", systemImage: "drop.fill", value: AppTab.today) { TodayView() }
            Tab("History", systemImage: "calendar", value: AppTab.history) { HistoryView() }
            Tab("Insights", systemImage: "chart.bar.fill", value: AppTab.insights) { InsightsView() }
            Tab("Add", systemImage: "plus", value: AppTab.add, role: .prominent) {   // iOS 27; use .search on 26
                Color.clear
            }
        }
        .tabBarMinimizeBehavior(.onScrollDown)                 // iOS 26 [17]
        .sheet(isPresented: $showAddSheet) {
            AddDrinkSheet()
                .presentationDetents([.height(340), .medium, .large])
                .presentationDragIndicator(.visible)
        }
    }
}
```
If the setter-interception ever lets the selection change visually, the fallback is `.onChange(of: selection) { old, new in if new == .add { selection = old; showAddSheet = true } }`.

### 3.2 Tab bar minimize and bottom accessory

- `tabBarMinimizeBehavior(_:)` (iOS 26) with `.onScrollDown` etc. [17].
- `tabViewBottomAccessory { }` (iOS 26). `tabViewBottomAccessory(isEnabled:content:)` was added in iOS **26.1** [18]. Read the `\.tabViewBottomAccessoryPlacement` environment value to adapt when the accessory moves inline with the minimized bar.

```swift
TabView { … }
  .tabViewBottomAccessory {
      QuickAddBar()     // e.g. "+250 ml  +500 ml  ☕︎" chips; HIG-friendly home for actions
  }
```

### 3.3 Glass effects, containers, morphing, button styles

All iOS 26+: `glassEffect(_:in:)` [19], `Glass` (`.regular`, `.clear`, `.identity`, `.tint(_:)`, `.interactive(_:)`) [22], `GlassEffectContainer(spacing:)` [20], `glassEffectID(_:in:)` [21], `glassEffectUnion(id:namespace:)`, `glassEffectTransition(_:)`, `.buttonStyle(.glass)` [23], `.buttonStyle(.glassProminent)` [24].

```swift
struct QuickAddCluster: View {
    @Namespace private var glass
    @State private var expanded = false

    var body: some View {
        GlassEffectContainer(spacing: 12) {
            HStack(spacing: 12) {
                if expanded {
                    ForEach(Preset.all) { p in
                        Button { log(p) } label: { Label(p.title, systemImage: p.symbol) }
                            .buttonStyle(.glass)
                            .glassEffectID(p.id, in: glass)
                    }
                }
                Button { withAnimation(.bouncy) { expanded.toggle() } } label: {
                    Image(systemName: expanded ? "xmark" : "plus").font(.title2.bold())
                        .frame(width: 56, height: 56)
                }
                .glassEffect(.regular.tint(.cyan).interactive(), in: .circle)
                .glassEffectID("toggle", in: glass)
            }
        }
    }
}
```

HIG: use Liquid Glass **only for the functional layer** (controls/navigation) and sparingly. Don't use it for content such as cards. Use `.clear` only over rich media, with a ~35% dimming layer behind it when the content is bright [34]. A water-progress ring belongs in the content layer, so use standard materials or solid fills for it.

### 3.4 Sheets

- System sheets adopt glass automatically. Half sheets are inset from the screen edges and become more opaque at full height [28].
- **Remove custom `presentationBackground` and visual-effect views** so the system glass shows [28].
- Zoom from the source button: `.matchedTransitionSource(id:in:)` on the button plus `.navigationTransition(.zoom(sourceID:in:))` on the sheet content (iOS 18+). WWDC25 shows sheets morphing out of toolbar buttons [30].
- WWDC26 "Sheet Placement" was listed in a third-party catalog only. I found no Apple symbol (**unverified**).

```swift
@Namespace private var ns
Button("Add", systemImage: "plus") { showAdd = true }
    .matchedTransitionSource(id: "add", in: ns)
.sheet(isPresented: $showAdd) {
    AddDrinkSheet()
        .presentationDetents([.medium, .large])
        .navigationTransition(.zoom(sourceID: "add", in: ns))
}
```

### 3.5 Toolbars

- iOS 26: items are grouped on shared glass backgrounds. Use `ToolbarSpacer(.fixed | .flexible)` to split groups [25], and `.sharedBackgroundVisibility(.hidden)` on a `ToolbarContent` to pull one item out of the shared glass.
- **iOS 27 (WWDC26) [29]:** `ToolbarItemPlacement.topBarPinnedTrailing` [35], `ToolbarOverflowMenu { }` [36] and `ToolbarContent.visibilityPriority(.high)` [37] are all in the docs with iOS 27.0 availability. **`toolbarMinimizeBehavior(.onScrollDown, for: .navigationBar)` was shown in the session but returns 404 in the docs index (unverified)**, so check it in Xcode 27.

```swift
.toolbar {
    ToolbarItem(placement: .topBarLeading) { Button("Settings", systemImage: "gearshape") { … } }
    ToolbarItemGroup(placement: .topBarTrailing) {
        Button("Undo", systemImage: "arrow.uturn.backward") { undoLast() }
    }
    .visibilityPriority(.high)                     // iOS 27
    ToolbarSpacer(.fixed)
    ToolbarItem(placement: .topBarPinnedTrailing) { // iOS 27
        Button("Add", systemImage: "plus") { showAdd = true }.buttonStyle(.glassProminent)
    }
}
```

### 3.6 Scroll edge effects and custom bars

- `scrollEdgeEffectStyle(_:for:)` (`.automatic`, `.soft`, `.hard`) [26] and `scrollEdgeEffectHidden(_:for:)` (iOS 26).
- For a custom bottom bar over scrolling content, use `safeAreaBar(edge:alignment:spacing:content:)` (iOS 26) [27]. It registers the bar so the system applies the edge effect, which `safeAreaInset` doesn't.
- `backgroundExtensionEffect()` (iOS 26) mirrors and blurs a hero image under bars and sidebars.

### 3.7 Other iOS 27 / WWDC26 SwiftUI changes relevant to Hydrate [29]

- Liquid Glass refresh applies automatically on rebuild with the iOS 27 SDK. Custom glass can be "interactive" (`Glass.interactive`) and a new system glass slider exists.
- `.reorderable()` + `.reorderContainer(for:)` let users reorder drink presets in any container.
- `.swipeActions` outside `List` (with `.swipeActionsContainer()` on the ScrollView), for swipe-to-delete in a custom history list.
- `alert`/`confirmationDialog(item:)` for "Delete this drink?".
- `@State` is now a macro with lazy class init. It's source-breaking if a property has a default value **and** is assigned in `init`.
- `ContentBuilder` unifies result builders, which speeds up type-checking.

---

## 4. Widgets and App Intents, the Apple way

### 4.1 One intent for everything

```swift
import AppIntents

enum DrinkKind: String, AppEnum {
    case water, coffee, tea, juice, soda, milk
    static let typeDisplayRepresentation: TypeDisplayRepresentation = "Drink"
    static let caseDisplayRepresentations: [DrinkKind: DisplayRepresentation] = [
        .water: "Water", .coffee: "Coffee", .tea: "Tea", .juice: "Juice", .soda: "Soda", .milk: "Milk"
    ]
}

enum ServingSize: String, AppEnum {          // finite set => usable inside Siri phrases
    case sip, glass, mug, bottle
    static let typeDisplayRepresentation: TypeDisplayRepresentation = "Serving"
    static let caseDisplayRepresentations: [ServingSize: DisplayRepresentation] = [
        .sip: "sip (100 ml)", .glass: "glass (250 ml)", .mug: "mug (350 ml)", .bottle: "bottle (500 ml)"
    ]
}

struct LogDrinkIntent: AppIntent {
    static let title: LocalizedStringResource = "Log Drink"
    static let description = IntentDescription("Logs a drink in Hydrate.")
    static let supportedModes: IntentModes = .background          // iOS 26 [45]

    @Parameter(title: "Drink", default: .water) var drink: DrinkKind
    @Parameter(title: "Serving", default: .glass) var serving: ServingSize
    @Parameter(title: "Amount (ml)") var customML: Int?           // asked by Siri/Shortcuts if needed

    init() {}
    init(drink: DrinkKind, serving: ServingSize) { self.drink = drink; self.serving = serving }

    func perform() async throws -> some IntentResult & ProvidesDialog {
        let ml = customML ?? serving.milliliters
        try await DrinkStore.shared.log(kind: drink, ml: ml, source: .intent)   // SwiftData in App Group
        WidgetCenter.shared.reloadAllTimelines()
        ControlCenter.shared.reloadAllControls()
        let total = try await DrinkStore.shared.todayTotalML()
        return .result(dialog: "Logged \(ml) ml of \(drink.localizedName). \(total) ml today.")
    }
}
```
Widgets don't resolve parameters, so the values have to be preset in the widget's `Button(intent:)` [38]. The intent file must be a member of **both** the app and the widget extension target [38].

### 4.2 Interactive Home Screen and Lock Screen widgets

- `Button(intent:)` / `Toggle(isOn:intent:)` (iOS 17+). Supported families: systemSmall through systemExtraLarge(Portrait), plus **`accessoryCircular` and `accessoryRectangular` on iPhone/iPad** [38]. On a locked device, buttons do nothing until the user authenticates [38].
- After `perform()` returns, the system reloads the timeline. Finish the SwiftData save *before* returning [38]. Use `.invalidatableContent()` on the total label.
- StandBy shows systemSmall widgets. iOS 27 adds `systemExtraLargePortrait` [75].
- Accessory widgets render in vibrant/accented modes. Check `\.widgetRenderingMode` and use `widgetAccentable()`.

```swift
struct TodayWidgetView: View {
    let entry: HydrationEntry
    @Environment(\.widgetFamily) private var family
    var body: some View {
        switch family {
        case .accessoryCircular:
            Gauge(value: entry.progress) { Image(systemName: "drop.fill") }
                .gaugeStyle(.accessoryCircularCapacity)
        default:
            VStack(alignment: .leading) {
                Text("\(entry.totalML) / \(entry.goalML) ml").font(.headline).invalidatableContent()
                HStack {
                    Button(intent: LogDrinkIntent(drink: .water, serving: .glass)) { Label("250", systemImage: "drop.fill") }
                    Button(intent: LogDrinkIntent(drink: .water, serving: .bottle)) { Label("500", systemImage: "waterbottle.fill") }
                }
                .buttonStyle(.bordered)
            }
            .containerBackground(.fill.tertiary, for: .widget)
        }
    }
}
```

### 4.3 Control Center / Lock Screen / Action button controls

```swift
import WidgetKit
import SwiftUI

struct QuickLogControl: ControlWidget {
    var body: some ControlWidgetConfiguration {
        StaticControlConfiguration(kind: "hydrate.control.quicklog") {
            ControlWidgetButton(action: LogDrinkIntent(drink: .water, serving: .glass)) {
                Label("Log Glass", systemImage: "drop.fill")
            }
        }
        .displayName("Log Water")
        .description("Adds a 250 ml glass of water.")
    }
}
```
`ControlWidget` (iOS 18) lives in SwiftUI, and `ControlWidgetButton`/`StaticControlConfiguration` in WidgetKit [39][40][41]. Use `AppIntentControlConfiguration` with a configurable intent if you want the user to choose the serving size when adding the control.

### 4.4 App Shortcuts (zero-setup phrases)

```swift
struct HydrateShortcuts: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(intent: LogDrinkIntent(),
                    phrases: [
                        "Log a glass of water in \(.applicationName)",
                        "Log \(\.$serving) of water in \(.applicationName)",
                        "Log \(\.$drink) in \(.applicationName)"
                    ],
                    shortTitle: "Log Drink",
                    systemImageName: "drop.fill")
        AppShortcut(intent: TodayTotalIntent(),
                    phrases: ["How much have I drunk in \(.applicationName)"],
                    shortTitle: "Today's Total",
                    systemImageName: "chart.bar.fill")
    }
}
```
Rules from WWDC22/23 that the docs don't restate: every phrase must contain `\(.applicationName)`. Only finite `AppEnum`/`AppEntity` parameters can appear inside phrases, so a free-form ml number can't, and Siri will ask for it instead. Apps are capped at 10 App Shortcuts. Call `HydrateShortcuts.updateAppShortcutParameters()` when dynamic entity options change [42]. `SiriTipView` advertises a phrase inside the app [43].

### 4.5 Where the intent runs (important for HealthKit)

- By default a widget/control intent runs **in the widget extension process** [38]. It can write the shared SwiftData store, but it **can't prompt for HealthKit** [15].
- To run in the app process, use `supportedModes = .background` (iOS 26) [45] or, on **iOS 27**, `static var allowedExecutionTargets: IntentExecutionTargets` restricted to the main app (`.main`) [46][47]. WWDC26 used `.main` for writes from a widget button [47]. Running in the app process lets the intent push to HealthKit immediately.
- Recommended: put the intent in both targets. Always write SwiftData first (fast, works anywhere), then push to HealthKit if `HKHealthStore.authorizationStatus(for: water) == .sharingAuthorized`; otherwise leave it in the outbox.

### 4.6 Apple Intelligence / Siri changes (iOS 26–27)

- **App schemas (formerly assistant schemas):** the domain list as of Nov 2026 has primary domains Audio, Calendar, Camera, Clock, Mail, Maps, Messages, Notes, Phone, Photos, Reminders, Search and Video, plus Shortcuts-only domains such as Journaling and Files. **There's no health, nutrition or logging domain** [48][49], so Hydrate uses plain App Intents.
- **WWDC26 App Intents additions** [47]: `EntityCollection`, `SyncableEntity`, `RelevantEntities`, `@UnionValue`, native `Duration` params, `LongRunningIntent` (avoid; it uses a Live Activity), `CancellableIntent`, `allowedExecutionTargets`.
- **Siri AI Developer Preview (2026-11-03, iOS 27.3 beta):** `ToolIntent` / `@AppIntent(.tool)` promote an existing intent to a Siri "tool," with a title, description and per-parameter descriptions. "App skills" are `SKILL.md` files. It needs an Apple Intelligence device and development-signed builds. Reportedly no new entitlement [50][51]. `ToolIntent` shows iOS **27.3** availability [50]. That's above Hydrate's 27.2 target, so it's optional. Per [50], the macro adds a conformance carrying ToolIntent's availability, so it should be safe to adopt later. LogDrinkIntent is a near-perfect candidate ("Log two glasses of water").

### 4.7 Data sharing between app and widgets

- **App Group container (available on free teams [1][3]).** Point SwiftData at it with `ModelConfiguration(groupContainer: .identifier(appGroupID))` [54], or `.automatic`, which uses the app's primary group [54]. Small settings like goal and units go in `UserDefaults(suiteName: appGroupID)`.
- If App Groups ever fail to provision, the fallbacks are weak. Keychain Sharing (free [1]) can carry a few values such as today's total and goal, but not a store. The widget could show a static "Open Hydrate" state, and intents could be forced into the app process with `allowedExecutionTargets` [46]. Treat App Groups as required and smoke-test them first.

---

## 5. Data layer: SwiftData on iOS 26/27

### 5.1 Model sketch

```swift
import SwiftData

enum HydrateSchemaV1: VersionedSchema {
    static var versionIdentifier = Schema.Version(1, 0, 0)
    static var models: [any PersistentModel.Type] { [DrinkLog.self, DrinkPreset.self, ProfileSnapshot.self, DailyGoal.self, ExternalWaterSample.self] }

    @Model final class DrinkLog {
        #Unique<DrinkLog>([\.id])                         // iOS 18 [57]
        #Index<DrinkLog>([\.timestamp], [\.dayKey])       // iOS 18 [56]
        var id: UUID = UUID()
        var timestamp: Date = Date.now
        var dayKey: Int = 0                    // yyyymmdd in the user's calendar at log time (stable across TZ changes)
        var drinkTypeRaw: String = "water"
        var drinkName: String = "Water"
        var volumeML: Double = 0
        var waterFraction: Double = 1.0        // effective water = volumeML * waterFraction
        var caffeineMG: Double?
        var sugarG: Double?
        var sourceRaw: String = "app"          // app | widget | control | siri | import
        var syncVersion: Int = 1               // HealthKit HKMetadataKeySyncVersion
        var healthStateRaw: String = "pending" // pending | synced | pendingDelete | failed
        var deletedAt: Date?                   // soft delete until HealthKit delete succeeds
        init() {}
        var effectiveWaterML: Double { volumeML * waterFraction }
    }

    @Model final class ProfileSnapshot {        // history so past goals stay explainable
        var effectiveFrom: Date = Date.now
        var weightKG: Double?
        var activityLevelRaw: String = "moderate"
        var climateRaw: String = "temperate"
        init() {}
    }

    @Model final class DailyGoal {              // goal frozen per day; totals are computed, not stored
        #Unique<DailyGoal>([\.dayKey])
        var dayKey: Int = 0
        var goalML: Double = 2000
        init() {}
    }
    // DrinkPreset, ExternalWaterSample (keyed by HealthKit UUID) …
}
```
Design notes:
- **Don't store daily totals.** Compute them with a `#Predicate` on `dayKey` and sum, or with an iOS 27 sectioned `@Query(sectionBy:)` [62]. Store only the **goal** per day (`DailyGoal`) so history doesn't change when the profile changes.
- Use `dayKey` rather than `startOfDay` `Date` comparisons, so time-zone travel doesn't move past drinks to another day.
- Give every property a default value. It makes migrations and any future CloudKit move easier. (CloudKit also forbids `#Unique`, but that doesn't matter on a free team.)
- iOS 27: `@Attribute(.codable)` stores Codable types, but they can't be used in predicates, sorting or migration [63]. Enum predicates now work directly [62], so `drinkType` could become a stored enum. Keep a raw string in v1 for export stability.

### 5.2 Migration and versioning

Start with `VersionedSchema` + `SchemaMigrationPlan` on day one [58][59]. Add `HydrateSchemaV2` plus a `MigrationStage.lightweight` or `.custom` stage when models change. WWDC25 covers inheritance and migration [61].

```swift
enum HydrateMigrationPlan: SchemaMigrationPlan {
    static var schemas: [any VersionedSchema.Type] { [HydrateSchemaV1.self] }
    static var stages: [MigrationStage] { [] }
}

let config = ModelConfiguration("Hydrate",
                                schema: Schema(versionedSchema: HydrateSchemaV1.self),
                                isStoredInMemoryOnly: false,
                                allowsSave: true,
                                groupContainer: .identifier(AppGroup.id),
                                cloudKitDatabase: .none)          // be explicit: no iCloud on free team [55]
let container = try ModelContainer(for: Schema(versionedSchema: HydrateSchemaV1.self),
                                   migrationPlan: HydrateMigrationPlan.self,
                                   configurations: config)
```

### 5.3 SwiftData from widgets and intents

- Build the **same** container (shared factory in a framework or a shared file) in the app, the widget extension and intents. Open a fresh `ModelContext` per timeline request or intent and keep it short-lived.
- **Cross-process staleness:** the app's `@Query` doesn't reliably refresh when the widget process writes. On `scenePhase == .active`, read persistent history (`HistoryDescriptor`, iOS 18 [60]). iOS 27's `HistoryObserver` / `ResultsObserver` [62] are designed for this. Or just refetch.
- After any in-app write, call `WidgetCenter.shared.reloadTimelines(ofKind:)` and `ControlCenter.shared.reload…`.
- Community-reported iOS 27 issues: `propertiesToFetch` still fetches everything, and `ModelActor` sometimes runs on main [63]. Don't rely on them for performance.

### 5.4 SwiftData + CloudKit on a free team?

**No.** It needs the iCloud (CloudKit) capability, which free teams don't have [1]. Keep `cloudKitDatabase: .none`. If you join the paid program later, switching to `.private("iCloud.<id>")` is a config change, provided the model already follows CloudKit's rules: defaults or optionals everywhere, no `#Unique`, optional relationships.

---

## 6. Other

### 6.1 App icons (iOS 26+)

- **Icon Composer `.icon`** is one layered file that renders the **Default, Dark and Mono** appearances. Mono covers the **Clear** (light/dark) and **Tinted** variants. Xcode generates fallback images for older OS versions [69][70][71]. Up to 4 layer groups. Export layers as SVG, without blur or shadows.
- **Alternate icons:** Apple's current sample uses **one `.icon` file per alternate icon**. List them in the build setting *Alternate App Icon Sets* (`ASSETCATALOG_COMPILER_ALTERNATE_APPICON_NAMES`), not by hand-editing `CFBundleAlternateIcons`, then call `UIApplication.shared.setAlternateIconName(_:)` [67][68]. Early Xcode 26 betas had bugs with `.icon` alternate icons [79]. The sample suggests it's fixed, but test it. The system shows its own alert on every icon change.

```swift
Button("Ocean") {
    UIApplication.shared.setAlternateIconName("AppIcon-Ocean") { error in
        if let error { logger.error("Icon change failed: \(error)") }
    }
}
// nil restores the primary icon; current: UIApplication.shared.alternateIconName
```

### 6.2 Local notification reminders (smart scheduling)

- No entitlement needed. Ask for permission after onboarding shows the value. Time Sensitive isn't available on a free team [1].
- **Smart scheduling:** each time a drink is logged (in the app, an intent or the widget) and on foreground, recompute the next reminders. Leave out reminders when the user is ahead of the pro-rated goal. Only schedule inside the wake window (e.g. 08:00–21:00). Use `UNCalendarNotificationTrigger` for fixed times and `UNTimeIntervalNotificationTrigger` for "nudge in 90 min if nothing logged" [72].
- Keep under the long-standing **64 pending local notifications per app** limit (legacy documentation; I didn't find it on current pages, so treat it as unverified for iOS 27). Schedule about 1–2 days ahead and top up in `BGAppRefreshTask` or on app open.
- Add a `UNNotificationCategory` with actions "+250 ml" and "Snooze." Handle the action in `userNotificationCenter(_:didReceive:)` so it logs without opening the UI.
- Widgets and intents can't reliably reschedule notifications from the extension. Set an "reschedule needed" flag in the App Group, and have the app or BG task act on it.

### 6.3 HIG highlights

- **Liquid Glass / Materials** [34]: glass is for the navigation and control layer only, used sparingly. `.regular` is the default, and `.clear` is only for over media. Standard components adopt it automatically, so remove custom bar backgrounds [28].
- **Tab bars** [33]: navigation, not actions. A dedicated search tab sits at the trailing end. The minimize behavior suits apps with an accessory. Change log: Liquid Glass guidance added 2025-07-28, updated 2025-12-16 and 2026-06-08.
- **Onboarding** [73]: keep it fast, fun and optional, and teach through interaction (log your first glass). Prefer TipKit tips over a long flow. Request permissions (Health, notifications) in context, explaining the benefit. Postpone non-essential setup and provide sensible defaults (2,000 ml goal until a weight is known).
- **Charts** [74]: highlight a few key insights. Use bar marks to compare days, and a line or rule mark for the goal. Add axis labels, titles and accessibility labels (Swift Charts supports audio graphs). Weekly bars with a `RuleMark` at the goal is the canonical hydration chart.

---

## Risks / unknowns

1. **HealthKit Background Delivery entitlement on a free team:** unverified. Design the app to work without it (foreground refresh plus anchored queries).
2. **App Groups provisioning on free teams:** Apple's table and DTS say yes [1][3]. Community reports conflict, including empty group lists that are mostly from sideload tools. A one-group-per-app limit is reported [5]. **Smoke-test before building on it.**
3. **Siri voice invocation of App Shortcuts without the Siri capability:** expected to work. One contrary third-party report [77]. Test on device.
4. **`Tab(role: .search)` used as an action button:** behavior with an intercepted selection and no `.searchable` is unverified. `.prominent` (iOS 27) is the cleaner choice, but both go against the HIG's "navigation, not actions" guidance [33].
5. **`toolbarMinimizeBehavior`** was demoed at WWDC26 [29] but isn't in the docs index. The "Sheet Placement" API is unverified.
6. **`fileExporter(… document: FileDocument …)`** is marked deprecated as of the 27.3 SDK [64]. Use the `Transferable` `item:` overloads [65].
7. **Siri AI tools (`ToolIntent`)** are a 27.3 *beta* preview. APIs and behavior may change, and terms aren't published yet [51].
8. **7-day expiry:** if you forget to reinstall, the app and its widgets stop working, and **reminders won't fire** while the app can't launch. This doesn't cause data loss, but goals and streaks can show gaps.
9. **Bundle-ID changes** (e.g. a friend forks the project) create a new data container and a new HealthKit source. Export/import and metadata-based HealthKit restore are the migration path.
10. **Cross-process SwiftData freshness:** widget writes may not appear in the app's `@Query` until a refetch. Use persistent history or iOS 27 observers [60][62].
11. Several WWDC26 summaries came from third-party blogs. Every API name in this document was checked against Apple's doc index unless marked unverified.

---

## References

1. Apple — Supported capabilities (iOS). https://developer.apple.com/help/account/reference/supported-capabilities-ios (parsed 2026-11-13)
2. Apple — Choosing a membership (free-tier limits: 10 App IDs, 3 devices, 3 apps, 7-day profiles). https://developer.apple.com/support/compare-memberships/
3. Apple Developer Forums — "Failed to register bundle identifier" for teammates (HealthKit + App Groups on personal teams; DTS reply, June 2026). https://developer.apple.com/forums/thread/834802
4. Apple Developer Forums — xcode app limit (DTS on Personal Team App ID limits, Jan 2024). https://developer.apple.com/forums/thread/745359
5. xtool PR #284 — "Allow one app group on free teams" (tested on iOS 27.2, merged 2026-10-30; third-party). https://github.com/xtool-org/xtool/pull/284
6. HealthKit — HKMetadataKeySyncIdentifier. https://developer.apple.com/documentation/healthkit/hkmetadatakeysyncidentifier
7. HealthKit — HKMetadataKeySyncVersion. https://developer.apple.com/documentation/healthkit/hkmetadatakeysyncversion
8. HealthKit — dietaryWater. https://developer.apple.com/documentation/healthkit/hkquantitytypeidentifier/dietarywater
9. HealthKit — authorizationStatus(for:). https://developer.apple.com/documentation/healthkit/hkhealthstore/authorizationstatus(for:)
10. HealthKit — Protecting user privacy. https://developer.apple.com/documentation/healthkit/protecting-user-privacy
11. HealthKit — enableBackgroundDelivery(for:frequency:withCompletion:). https://developer.apple.com/documentation/healthkit/hkhealthstore/enablebackgrounddelivery(for:frequency:withcompletion:)
12. HealthKit — HKAnchoredObjectQueryDescriptor. https://developer.apple.com/documentation/healthkit/hkanchoredobjectquerydescriptor
13. HealthKit — deleteObjects(of:predicate:withCompletion:). https://developer.apple.com/documentation/healthkit/hkhealthstore/deleteobjects(of:predicate:withcompletion:)
14. SwiftUI — healthDataAccessRequest(store:shareTypes:readTypes:trigger:completion:). https://developer.apple.com/documentation/swiftui/view/healthdataaccessrequest(store:sharetypes:readtypes:trigger:completion:)
15. Apple Developer Forums — WidgetKit + HealthKit Authorization. https://developer.apple.com/forums/thread/653814
16. SwiftUI — TabRole.prominent (iOS 27). https://developer.apple.com/documentation/swiftui/tabrole/prominent
17. SwiftUI — tabBarMinimizeBehavior(_:). https://developer.apple.com/documentation/swiftui/view/tabbarminimizebehavior(_:)
18. SwiftUI — tabViewBottomAccessory(isEnabled:content:) (iOS 26.1). https://developer.apple.com/documentation/swiftui/view/tabviewbottomaccessory(isenabled:content:)
19. SwiftUI — glassEffect(_:in:). https://developer.apple.com/documentation/swiftui/view/glasseffect(_:in:)
20. SwiftUI — GlassEffectContainer. https://developer.apple.com/documentation/swiftui/glasseffectcontainer
21. SwiftUI — glassEffectID(_:in:). https://developer.apple.com/documentation/swiftui/view/glasseffectid(_:in:)
22. SwiftUI — Glass. https://developer.apple.com/documentation/swiftui/glass
23. SwiftUI — PrimitiveButtonStyle.glass. https://developer.apple.com/documentation/swiftui/primitivebuttonstyle/glass
24. SwiftUI — PrimitiveButtonStyle.glassProminent. https://developer.apple.com/documentation/swiftui/primitivebuttonstyle/glassprominent
25. SwiftUI — ToolbarSpacer. https://developer.apple.com/documentation/swiftui/toolbarspacer
26. SwiftUI — scrollEdgeEffectStyle(_:for:). https://developer.apple.com/documentation/swiftui/view/scrolledgeeffectstyle(_:for:)
27. SwiftUI — safeAreaBar(edge:alignment:spacing:content:). https://developer.apple.com/documentation/swiftui/view/safeareabar(edge:alignment:spacing:content:)
28. Apple — Adopting Liquid Glass. https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass
29. WWDC26 — What's new in SwiftUI (session 269). https://developer.apple.com/videos/play/wwdc2026/269/
30. WWDC25 — Build a SwiftUI app with the new design (323). https://developer.apple.com/videos/play/wwdc2025/323/
31. WWDC25 — Meet Liquid Glass (219). https://developer.apple.com/videos/play/wwdc2025/219/
32. SwiftUI — TabSearchActivation / tabViewSearchActivation(_:). https://developer.apple.com/documentation/swiftui/tabsearchactivation
33. HIG — Tab bars (change log through 2026-06-08). https://developer.apple.com/design/human-interface-guidelines/tab-bars
34. HIG — Materials (Liquid Glass). https://developer.apple.com/design/human-interface-guidelines/materials
35. SwiftUI — ToolbarItemPlacement.topBarPinnedTrailing (iOS 27). https://developer.apple.com/documentation/swiftui/toolbaritemplacement/topbarpinnedtrailing
36. SwiftUI — ToolbarOverflowMenu (iOS 27). https://developer.apple.com/documentation/swiftui/toolbaroverflowmenu
37. SwiftUI — ToolbarContent.visibilityPriority(_:) (iOS 27). https://developer.apple.com/documentation/swiftui/toolbarcontent/visibilitypriority(_:)
38. WidgetKit — Adding interactivity to widgets and Live Activities. https://developer.apple.com/documentation/widgetkit/adding-interactivity-to-widgets-and-live-activities
39. WidgetKit — ControlWidgetButton. https://developer.apple.com/documentation/widgetkit/controlwidgetbutton
40. WidgetKit — StaticControlConfiguration. https://developer.apple.com/documentation/widgetkit/staticcontrolconfiguration
41. WWDC24 — Extend your app's controls across the system (10157). https://developer.apple.com/videos/play/wwdc2024/10157/
42. App Intents — AppShortcutsProvider. https://developer.apple.com/documentation/appintents/appshortcutsprovider
43. App Intents — App Shortcuts. https://developer.apple.com/documentation/appintents/app-shortcuts
44. App Intents — AppEnum. https://developer.apple.com/documentation/appintents/appenum
45. App Intents — AppIntent.supportedModes (iOS 26). https://developer.apple.com/documentation/appintents/appintent/supportedmodes
46. App Intents — AppIntent.allowedExecutionTargets (iOS 27). https://developer.apple.com/documentation/appintents/appintent/allowedexecutiontargets
47. WWDC26 — Discover new capabilities in the App Intents framework (345). https://developer.apple.com/videos/play/wwdc2026/345/
48. App Intents — App schema domains. https://developer.apple.com/documentation/appintents/app-schema-domains
49. WWDC26 — Build intelligent Siri experiences with App Schemas (240). https://developer.apple.com/videos/play/wwdc2026/240/
50. App Intents — ToolIntent (iOS 27.3) and AppIntent(_:) macro. https://developer.apple.com/documentation/appintents/toolintent
51. PPC Land — "Apple opens Siri AI to all developers…" (2026-11-03 developer preview summary; secondary). https://ppc.land/apple-opens-siri-ai-to-all-developers-but-apps-cant-ship-it-until-spring/
52. WWDC25 — Get to know App Intents (244). https://developer.apple.com/videos/play/wwdc2025/244/
53. WWDC25 — Explore new advances in App Intents (275). https://developer.apple.com/videos/play/wwdc2025/275/
54. SwiftData — ModelConfiguration.GroupContainer. https://developer.apple.com/documentation/swiftdata/modelconfiguration/groupcontainer-swift.struct
55. SwiftData — ModelConfiguration. https://developer.apple.com/documentation/swiftdata/modelconfiguration
56. SwiftData — Index(_:) macro. https://developer.apple.com/documentation/swiftdata/index(_:)-74ia2
57. SwiftData — Unique(_:) macro. https://developer.apple.com/documentation/swiftdata/unique(_:)
58. SwiftData — VersionedSchema. https://developer.apple.com/documentation/swiftdata/versionedschema
59. SwiftData — SchemaMigrationPlan. https://developer.apple.com/documentation/swiftdata/schemamigrationplan
60. SwiftData — HistoryDescriptor. https://developer.apple.com/documentation/swiftdata/historydescriptor
61. WWDC25 — SwiftData: Dive into inheritance and schema migration (291). https://developer.apple.com/videos/play/wwdc2025/291/
62. WWDC26 — What's new in SwiftData (274). https://developer.apple.com/videos/play/wwdc2026/274/
63. Michael Tsai — SwiftData in appleOS 27 (2026-06-23; roundup of community findings). https://mjtsai.com/blog/2026/06/23/swiftdata-in-appleos-27/
64. SwiftUI — fileExporter(isPresented:document:contentType:defaultFilename:onCompletion:) (availability iOS 14.0–27.3). https://developer.apple.com/documentation/swiftui/view/fileexporter(ispresented:document:contenttype:defaultfilename:oncompletion:)
65. SwiftUI — fileExporter(isPresented:item:contentTypes:defaultFilename:onCompletion:onCancellation:) (iOS 17). https://developer.apple.com/documentation/swiftui/view/fileexporter(ispresented:item:contenttypes:defaultfilename:oncompletion:oncancellation:)
66. SwiftUI — fileImporter(isPresented:allowedContentTypes:allowsMultipleSelection:onCompletion:). https://developer.apple.com/documentation/swiftui/view/fileimporter(ispresented:allowedcontenttypes:allowsmultipleselection:oncompletion:)
67. UIKit — setAlternateIconName(_:completionHandler:). https://developer.apple.com/documentation/uikit/uiapplication/setalternateiconname(_:completionhandler:)
68. Xcode sample — Configuring your app to use alternate app icons. https://developer.apple.com/documentation/xcode/configuring-your-app-to-use-alternate-app-icons
69. Xcode — Creating your app icon using Icon Composer. https://developer.apple.com/documentation/xcode/creating-your-app-icon-using-icon-composer
70. WWDC25 — Say hello to the new look of app icons (220). https://developer.apple.com/videos/play/wwdc2025/220/
71. WWDC25 — Create icons with Icon Composer (361). https://developer.apple.com/videos/play/wwdc2025/361/
72. UserNotifications — UNUserNotificationCenter. https://developer.apple.com/documentation/usernotifications/unusernotificationcenter
73. HIG — Onboarding. https://developer.apple.com/design/human-interface-guidelines/onboarding
74. HIG — Charts. https://developer.apple.com/design/human-interface-guidelines/charts
75. WWDC26 — WidgetKit foundations (277). https://developer.apple.com/videos/play/wwdc2026/277/
76. WWDC25 — What's new in widgets (278). https://developer.apple.com/videos/play/wwdc2025/278/
77. GitHub issue — Maui.Apple.PlatformFeature.Samples #1 (claim that Siri voice invocation needs the Siri entitlement; third-party, unverified). https://github.com/Redth/Maui.Apple.PlatformFeature.Samples/issues/1
78. WidgetKit — WidgetFamily.accessoryCircular. https://developer.apple.com/documentation/widgetkit/widgetfamily/accessorycircular
79. Apple Developer Forums — Can setAlternateIconName use .icon file? (unanswered; Xcode 26 beta era). https://developer.apple.com/forums/thread/790273
