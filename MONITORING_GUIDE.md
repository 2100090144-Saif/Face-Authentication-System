# 📊 Face Authentication Monitoring Guide

## 🔍 **Quick Log Analysis**

### **View Real-Time Logs**
```bash
# Follow all logs
docker-compose logs -f

# Follow only face_auth_app
docker logs -f face_auth_app

# Last 100 lines
docker logs --tail 100 face_auth_app
```

---

## 📋 **Log Patterns to Monitor**

### **1. Successful Authentication**
```bash
docker logs face_auth_app | grep "FINAL_DECISION.*ALLOW"
```

**Expected Output:**
```
[A1B2C3D4] STEP=FINAL_DECISION DECISION=ALLOW Authentication successful
username=john_doe, confidence=0.9234, confidence_pct=92.3%
```

---

### **2. Failed Authentication (Unknown Person)**
```bash
docker logs face_auth_app | grep "TOLERANCE_GATE.*REJECT"
```

**Expected Output:**
```
[E5F6G7H8] STEP=TOLERANCE_GATE DECISION=REJECT No match within tolerance=0.35
confidence=0.2145
```

---

### **3. Low Confidence Rejection**
```bash
docker logs face_auth_app | grep "CONFIDENCE_GATE.*REJECT"
```

**Expected Output:**
```
[I9J0K1L2] STEP=CONFIDENCE_GATE DECISION=REJECT Confidence 0.7234 < required 0.85
```

---

### **4. All Authentication Attempts**
```bash
docker logs face_auth_app | grep "STEP=START"
```

**Expected Output:**
```
[A1B2C3D4] STEP=START DECISION=INFO New face authentication attempt | timestamp=2026-04-22T07:15:23
[E5F6G7H8] STEP=START DECISION=INFO New face authentication attempt | timestamp=2026-04-22T07:16:45
```

---

### **5. Rate Limiting Events**
```bash
docker logs face_auth_app | grep "rate limit"
```

**Expected Output:**
```
Rate limit exceeded for IP 192.168.1.100: 5 attempts in 60 seconds
```

---

### **6. Detailed Match Analysis**
```bash
docker logs face_auth_app | grep "Candidate"
```

**Expected Output:**
```
Candidate 0: distance=0.4521, confidence=0.5479, within_tolerance=False
Candidate 1: distance=0.2845, confidence=0.7155, within_tolerance=True
Candidate 2: distance=0.5123, confidence=0.4877, within_tolerance=False
```

---

## 🚨 **Security Alerts to Watch**

### **⚠️ Alert 1: Multiple Failed Attempts from Same IP**
```bash
docker logs face_auth_app | grep "REJECT" | grep -o "timestamp=[^|]*" | sort | uniq -c | sort -rn
```

**Action**: Investigate if same IP has >10 failed attempts in short time

---

### **⚠️ Alert 2: Unknown Faces Getting High Confidence**
```bash
docker logs face_auth_app | grep "CONFIDENCE_GATE.*REJECT" | grep "confidence=0\.[8-9]"
```

**Action**: Review if tolerance threshold needs adjustment

---

### **⚠️ Alert 3: System Errors**
```bash
docker logs face_auth_app | grep "ERROR"
```

**Action**: Investigate any errors immediately

---

## 📈 **Statistics Commands**

### **Count Successful Logins Today**
```bash
docker logs face_auth_app | grep "$(date +%Y-%m-%d)" | grep "FINAL_DECISION.*ALLOW" | wc -l
```

### **Count Failed Attempts Today**
```bash
docker logs face_auth_app | grep "$(date +%Y-%m-%d)" | grep "DECISION=REJECT" | wc -l
```

### **Average Confidence for Successful Logins**
```bash
docker logs face_auth_app | grep "FINAL_DECISION.*ALLOW" | grep -o "confidence=[0-9.]*" | cut -d= -f2 | awk '{sum+=$1; count++} END {print sum/count}'
```

---

## 🔧 **Troubleshooting**

### **Issue: Unknown person getting logged in**

**Step 1**: Check if it actually happened
```bash
docker logs face_auth_app | grep "FINAL_DECISION.*ALLOW" | tail -20
```

**Step 2**: Get the attempt ID and trace full flow
```bash
# Replace A1B2C3D4 with actual attempt ID
docker logs face_auth_app | grep "\[A1B2C3D4\]"
```

**Step 3**: Verify all gates were checked
```bash
docker logs face_auth_app | grep "\[A1B2C3D4\]" | grep "GATE"
```

**Expected**: Should see TOLERANCE_GATE and CONFIDENCE_GATE checks

---

### **Issue: Legitimate user cannot log in**

**Step 1**: Find their recent attempts
```bash
docker logs face_auth_app | grep "username=john_doe" | tail -10
```

**Step 2**: Check confidence scores
```bash
docker logs face_auth_app | grep "username=john_doe" | grep "confidence="
```

**Step 3**: If confidence < 0.85, user may need to re-register face

---

## 📊 **Dashboard Queries**

### **Authentication Success Rate (Last Hour)**
```bash
#!/bin/bash
TOTAL=$(docker logs --since 1h face_auth_app | grep "STEP=START" | wc -l)
SUCCESS=$(docker logs --since 1h face_auth_app | grep "FINAL_DECISION.*ALLOW" | wc -l)
echo "Success Rate: $(echo "scale=2; $SUCCESS * 100 / $TOTAL" | bc)%"
```

### **Top 5 Users by Login Count**
```bash
docker logs face_auth_app | grep "FINAL_DECISION.*ALLOW" | grep -o "username=[^,]*" | sort | uniq -c | sort -rn | head -5
```

### **Peak Authentication Times**
```bash
docker logs face_auth_app | grep "STEP=START" | grep -o "[0-9][0-9]:[0-9][0-9]" | cut -d: -f1 | sort | uniq -c | sort -rn
```

---

## 🎯 **Security Monitoring Checklist**

Daily:
- [ ] Check for any ERROR logs
- [ ] Review failed authentication count
- [ ] Verify no suspicious patterns

Weekly:
- [ ] Analyze authentication success rate
- [ ] Review confidence score distribution
- [ ] Check for rate limiting events

Monthly:
- [ ] Review and adjust thresholds if needed
- [ ] Analyze user re-registration patterns
- [ ] Security audit of logs

---

## 📞 **Emergency Response**

### **If Unauthorized Access Detected:**

1. **Immediate**: Stop the container
   ```bash
   docker-compose down
   ```

2. **Investigate**: Extract all logs
   ```bash
   docker logs face_auth_app > security_incident_$(date +%Y%m%d_%H%M%S).log
   ```

3. **Analyze**: Find the breach attempt
   ```bash
   grep "FINAL_DECISION.*ALLOW" security_incident_*.log
   ```

4. **Remediate**: 
   - Review and tighten thresholds
   - Force all users to re-register faces
   - Update security policies

5. **Restart**: Only after fixes applied
   ```bash
   docker-compose up -d
   ```

---

**Last Updated**: 2026-04-22  
**Version**: 1.0
