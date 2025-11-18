package org.apache.commons.lang3.time;

import org.junit.Test;
import static org.junit.Assert.*;

public class FormatCacheTest {

    @Test
    public void testGetInstance_default() {
        FormatCache<java.text.Format> obj = new FormatCache<java.text.Format>() {
            @Override
            protected java.text.Format createInstance(String pattern, java.util.TimeZone timeZone, java.util.Locale locale) {
                return new java.text.SimpleDateFormat(pattern, locale);
            }
        };
        assertNotNull("getInstance() should not return null", obj.getInstance());
    }

    @Test
    public void testGetInstance_withParams() {
        FormatCache<java.text.Format> obj = new FormatCache<java.text.Format>() {
            @Override
            protected java.text.Format createInstance(String pattern, java.util.TimeZone timeZone, java.util.Locale locale) {
                return new java.text.SimpleDateFormat(pattern, locale);
            }
        };
        String pattern = "yyyy";
        java.util.TimeZone tz = java.util.TimeZone.getDefault();
        java.util.Locale locale = java.util.Locale.getDefault();
        assertNotNull("getInstance(pattern, tz, locale) should not return null",
                obj.getInstance(pattern, tz, locale));
    }

}