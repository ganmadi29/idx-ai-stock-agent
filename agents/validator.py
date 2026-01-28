class ValidatorAgent:
    def run(self, signal):
        if signal["volume_ratio"] >= 3:
            signal["confidence"] = "HIGH"
            return signal
        elif signal["volume_ratio"] >= 1.8:
            signal["confidence"] = "MEDIUM"
            return signal
        return None
