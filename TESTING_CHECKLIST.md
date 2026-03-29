# 🧪 Manual Testing Checklist

## Before Pushing to Repository

### 1. Service Tests
- [ ] Start geofence service: `bash start-geofence-service.sh`
- [ ] Check service status: `bash status-all-services.sh`
- [ ] View logs: `tail -f logs/geofence-service.log`
- [ ] Stop service: `bash stop-all-services.sh`

### 2. Indoor Service Tests
- [ ] Start indoor service: `bash start-indoor-service.sh`
- [ ] Verify WiFi detection works
- [ ] Test zone entry/exit notifications
- [ ] Stop service

### 3. Outdoor Service Tests
- [ ] Start outdoor service: `bash start-outdoor-service.sh`
- [ ] Verify GPS location updates
- [ ] Test zone breach detection
- [ ] Stop service

### 4. Notification Tests
- [ ] Receive Android notification on breach
- [ ] Camera app opens automatically
- [ ] Telegram notification received
- [ ] Notification buttons work

### 5. Camera Tests
- [ ] Camera app opens on breach
- [ ] Manual photo capture works
- [ ] Manual video recording works
- [ ] Files saved to correct directories

### 6. Configuration Tests
- [ ] Edit zones.json and reload
- [ ] Modify cooldown times
- [ ] Change active hours
- [ ] Test quiet hours (if enabled)

### 7. Edge Cases
- [ ] Service handles GPS timeout gracefully
- [ ] Service recovers from errors
- [ ] Multiple zone breaches handled
- [ ] Cooldown prevents spam

### 8. Documentation
- [ ] README.md is up to date
- [ ] All features documented
- [ ] Installation steps verified
- [ ] Examples work

## ✅ All Tests Passed - Ready to Push!
