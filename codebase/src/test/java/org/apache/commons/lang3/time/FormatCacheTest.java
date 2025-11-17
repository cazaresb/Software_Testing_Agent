package org.apache.commons.lang3.time;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class FormatCacheTest {

    @Test
    void test_getInstance() {
        // Arrange
        FormatCache obj = new FormatCache();

        // Act
        var result = obj.getInstance();

        // Assert
        // TODO: add meaningful assertions
        fail("Not yet implemented");
    }

    @Test
    void test_getInstance() {
        // Arrange
        FormatCache obj = new FormatCache();
        // TODO: initialize parameter 'pattern' of type 'String'
        // TODO: initialize parameter 'timeZone' of type 'TimeZone'
        // TODO: initialize parameter 'locale' of type 'Locale'

        // Act
        var result = obj.getInstance(pattern, timeZone, locale);

        // Assert
        // TODO: add meaningful assertions
        fail("Not yet implemented");
    }

}