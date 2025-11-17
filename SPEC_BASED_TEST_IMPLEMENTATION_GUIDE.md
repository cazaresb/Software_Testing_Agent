# Specification-Based Test Implementation Guide

**Project:** Apache Commons Lang 3.2-SNAPSHOT  
**Generated:** November 16, 2025  
**Test Framework:** JUnit 4 (Converted from spec-based analysis)

---

## Overview

This guide provides ready-to-implement JUnit 4 test templates generated from specification-based analysis. Each test includes:
- Test case specifications with boundary value analysis
- Equivalence class mapping
- Expected vs actual behavior descriptions
- TODO markers for assertion implementation

---

## Test Suite 1: TypeUtils Specification-Based Tests

**Class:** `org.apache.commons.lang3.reflect.TypeUtils`  
**Target Method:** `isAssignable(Type type, Type toType)`  
**Current Coverage:** 35% (CRITICAL)  
**Target Coverage:** 65%+

### Implementation File

**Path:** `codebase/src/test/java/org/apache/commons/lang3/reflect/TypeUtilsSpecTests.java`

```java
package org.apache.commons.lang3.reflect;

import org.junit.Before;
import org.junit.After;
import org.junit.Test;
import static org.junit.Assert.*;

import java.lang.reflect.Type;
import java.lang.reflect.ParameterizedType;
import java.util.List;

/**
 * Specification-Based Tests for TypeUtils
 * 
 * Focuses on boundary value analysis and equivalence class testing
 * for type assignability checking.
 * 
 * Coverage Target: 35% → 65%+
 * Test Cases: 12
 * Equivalence Classes: 7
 */
public class TypeUtilsSpecTests {
    
    // ============== Equivalence Class: Null Type Handling ==============
    
    /**
     * Spec: Null Type Parameters
     * Boundary: Both type and toType are null
     * Expected: Determine framework behavior (throw or return false)
     * BVA Class: Null equivalence class
     */
    @Test
    public void spec_01_bothTypesNull() {
        // TODO: Arrange - Set up null types
        // TODO: Act - Call TypeUtils.isAssignable(null, null)
        // TODO: Assert - Verify behavior (NPE vs false vs other)
    }
    
    /**
     * Spec: Null Source Type
     * Boundary: type is null, toType is valid
     * Expected: Handle null source
     */
    @Test
    public void spec_02_sourceTypeNull() {
        // TODO: Arrange
        // TODO: Act
        // TODO: Assert
    }
    
    /**
     * Spec: Null Target Type
     * Boundary: type is valid, toType is null
     * Expected: Handle null target
     */
    @Test
    public void spec_03_targetTypeNull() {
        // TODO: Arrange
        // TODO: Act
        // TODO: Assert
    }
    
    // ============== Equivalence Class: Identical Types ==============
    
    /**
     * Spec: Same Type Comparison
     * Boundary: type == toType (exact same class)
     * Expected: Return true - type is assignable to itself
     * BVA Class: Identity equivalence
     */
    @Test
    public void spec_04_identicalPrimitiveType() {
        // TODO: TypeUtils.isAssignable(int.class, int.class) → true
    }
    
    /**
     * Spec: Same Object Type
     * Boundary: Same reference object type
     * Expected: Return true
     */
    @Test
    public void spec_05_identicalObjectType() {
        // TODO: TypeUtils.isAssignable(String.class, String.class) → true
    }
    
    // ============== Equivalence Class: Superclass Assignment ==============
    
    /**
     * Spec: Subclass to Superclass
     * Boundary: Child class assignable to parent class
     * Expected: Return true (Integer extends Number)
     * BVA Class: Inheritance hierarchy
     */
    @Test
    public void spec_06_subclassToSuperclass() {
        // TODO: TypeUtils.isAssignable(Integer.class, Number.class) → true
        // TODO: TypeUtils.isAssignable(String.class, Object.class) → true
    }
    
    /**
     * Spec: Superclass to Subclass (Invalid)
     * Boundary: Parent class to child class (wrong direction)
     * Expected: Return false - not assignable
     * BVA Class: Reverse inheritance (invalid)
     */
    @Test
    public void spec_07_superclassToSubclass_invalid() {
        // TODO: TypeUtils.isAssignable(Number.class, Integer.class) → false
    }
    
    /**
     * Spec: Object Assignment
     * Boundary: Any class to Object
     * Expected: Return true - all classes inherit from Object
     * BVA Class: Universal superclass
     */
    @Test
    public void spec_08_anyToObject() {
        // TODO: TypeUtils.isAssignable(String.class, Object.class) → true
        // TODO: TypeUtils.isAssignable(int[].class, Object.class) → true
    }
    
    // ============== Equivalence Class: Autoboxing/Unboxing ==============
    
    /**
     * Spec: Primitive to Wrapper Assignment
     * Boundary: int to Integer conversion
     * Expected: Handle autoboxing (depends on implementation)
     * BVA Class: Type conversion
     */
    @Test
    public void spec_09_primitiveToWrapper() {
        // TODO: TypeUtils.isAssignable(int.class, Integer.class) → ?
        // TODO: Verify framework's autoboxing support
    }
    
    /**
     * Spec: Wrapper to Primitive
     * Boundary: Integer to int conversion
     * Expected: Unboxing behavior
     */
    @Test
    public void spec_10_wrapperToPrimitive() {
        // TODO: TypeUtils.isAssignable(Integer.class, int.class) → ?
    }
    
    // ============== Equivalence Class: Generic Types ==============
    
    /**
     * Spec: Generic Type Assignability
     * Boundary: List<String> to List<?> (wildcard)
     * Expected: Generic type handling
     * BVA Class: Parameterized types
     * COMPLEXITY: Higher - requires generic type support
     */
    @Test
    public void spec_11_genericToWildcard() {
        // TODO: Handle generic type parameters
        // TODO: Verify List<String> assignable to List<?>
    }
    
    /**
     * Spec: Raw vs Generic Type
     * Boundary: List (raw) vs List<String> (parameterized)
     * Expected: Framework-specific behavior
     */
    @Test
    public void spec_12_rawVsParameterized() {
        // TODO: TypeUtils.isAssignable(List.class, List.class) - raw types
        // TODO: TypeUtils.isAssignable(List.class, List<String>.class) - mixed
    }
    
    // ============== Test Lifecycle ==============
    
    @Before
    public void setUp() {
        // Initialize test fixtures
    }
    
    @After
    public void tearDown() {
        // Cleanup if needed
    }
}
```

---

## Test Suite 2: FastDatePrinter Specification-Based Tests

**Class:** `org.apache.commons.lang3.time.FastDatePrinter`  
**Target Method:** `format(Calendar calendar)`, `format(Date date)`, `format(long millis)`  
**Current Coverage:** 29-63% (CRITICAL)  
**Target Coverage:** 70%+

### Implementation File

**Path:** `codebase/src/test/java/org/apache/commons/lang3/time/FastDatePrinterSpecTests.java`

```java
package org.apache.commons.lang3.time;

import org.junit.Before;
import org.junit.After;
import org.junit.Test;
import static org.junit.Assert.*;

import java.util.Date;
import java.util.Calendar;
import java.util.TimeZone;
import java.util.Locale;
import java.text.SimpleDateFormat;

/**
 * Specification-Based Tests for FastDatePrinter
 * 
 * Boundary Value Analysis and Equivalence Class Testing
 * 
 * Coverage Target: 29-63% → 70%+
 * Test Cases: 15
 * Equivalence Classes: 6
 */
public class FastDatePrinterSpecTests {
    
    private FastDatePrinter printer;
    private static final String PATTERN_DATE = "yyyy-MM-dd";
    private static final String PATTERN_TIME = "HH:mm:ss";
    private static final String PATTERN_DATETIME = "yyyy-MM-dd HH:mm:ss";
    private static final String PATTERN_ISO8601 = "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'";
    
    // ============== Equivalence Class: Null Input Handling ==============
    
    /**
     * Spec: Null Date Object
     * Boundary: date parameter is null
     * Expected: NPE or graceful null handling
     */
    @Test(expected = NullPointerException.class)
    public void spec_01_nullDate_throwsException() {
        // TODO: printer.format((Date) null) should throw NPE
    }
    
    /**
     * Spec: Null Calendar Object
     * Boundary: calendar parameter is null
     * Expected: NPE or graceful handling
     */
    @Test(expected = NullPointerException.class)
    public void spec_02_nullCalendar_throwsException() {
        // TODO: printer.format((Calendar) null) should throw NPE
    }
    
    // ============== Equivalence Class: Standard Date Formatting ==============
    
    /**
     * Spec: Current Date Formatting
     * Boundary: Today's date
     * Expected: Formatted string matching pattern
     * BVA: Representative value
     */
    @Test
    public void spec_03_formatCurrentDate() {
        // TODO: printer = FastDatePrinter.getInstance("yyyy-MM-dd")
        // TODO: Date date = new Date()
        // TODO: String result = printer.format(date)
        // TODO: assertTrue(result matches pattern)
    }
    
    /**
     * Spec: Time-Only Formatting
     * Boundary: Time without date
     * Expected: Formatted time string
     */
    @Test
    public void spec_04_formatTimeOnly() {
        // TODO: printer = FastDatePrinter.getInstance("HH:mm:ss")
        // TODO: Verify time format without date components
    }
    
    /**
     * Spec: DateTime Formatting
     * Boundary: Combined date and time
     * Expected: Both components in output
     */
    @Test
    public void spec_05_formatDateTime() {
        // TODO: printer = FastDatePrinter.getInstance("yyyy-MM-dd HH:mm:ss")
        // TODO: Verify date and time both present
    }
    
    // ============== Equivalence Class: Edge Case Dates ==============
    
    /**
     * Spec: Epoch Date (1970-01-01)
     * Boundary: Minimum standard date
     * Expected: Format epoch correctly
     */
    @Test
    public void spec_06_formatEpoch() {
        // TODO: Date epoch = new Date(0L)
        // TODO: printer = FastDatePrinter.getInstance(PATTERN_DATE)
        // TODO: assertEquals("1970-01-01", printer.format(epoch))
    }
    
    /**
     * Spec: Year Boundary (9999)
     * Boundary: Max 4-digit year
     * Expected: Handle year 9999
     */
    @Test
    public void spec_07_formatMaxYear() {
        // TODO: Create calendar with year 9999
        // TODO: Verify formatting handles max year
    }
    
    /**
     * Spec: Leap Year Date (Feb 29)
     * Boundary: Leap day edge case
     * Expected: Format February 29 correctly
     */
    @Test
    public void spec_08_formatLeapDay() {
        // TODO: Calendar cal = Calendar.getInstance()
        // TODO: cal.set(2020, Calendar.FEBRUARY, 29)
        // TODO: String result = printer.format(cal)
        // TODO: assertTrue(result contains "02-29" or "29-02")
    }
    
    // ============== Equivalence Class: Timezone Handling ==============
    
    /**
     * Spec: UTC/Zulu Time Format
     * Boundary: ISO 8601 with Z suffix
     * Expected: UTC timezone representation
     */
    @Test
    public void spec_09_formatISO8601_UTC() {
        // TODO: FastDatePrinter utcPrinter = 
        //       FastDatePrinter.getInstance(PATTERN_ISO8601, TimeZone.getTimeZone("UTC"))
        // TODO: Verify Z or +00:00 suffix
    }
    
    /**
     * Spec: Timezone-Specific Formatting
     * Boundary: Different timezone (e.g., America/New_York)
     * Expected: Output adjusted for timezone
     */
    @Test
    public void spec_10_formatTimezone_EST() {
        // TODO: TimeZone est = TimeZone.getTimeZone("America/New_York")
        // TODO: FastDatePrinter tzPrinter = 
        //       FastDatePrinter.getInstance(PATTERN_DATETIME, est)
        // TODO: Verify timezone-adjusted output
    }
    
    /**
     * Spec: Daylight Saving Time Transition
     * Boundary: DST change boundary (e.g., Spring forward)
     * Expected: Correct time accounting for DST
     */
    @Test
    public void spec_11_formatDaylightSavingTime() {
        // TODO: Create calendar at DST transition (typically March 12 in US)
        // TODO: Verify time adjustment is correct
    }
    
    // ============== Equivalence Class: Locale-Specific Formatting ==============
    
    /**
     * Spec: US Date Format (MM/DD/YYYY)
     * Boundary: US locale
     * Expected: US-formatted date
     */
    @Test
    public void spec_12_formatUS_Locale() {
        // TODO: FastDatePrinter usPrinter = 
        //       FastDatePrinter.getInstance("MM/dd/yyyy", Locale.US)
        // TODO: Verify MM/DD/YYYY order
    }
    
    /**
     * Spec: European Date Format (DD/MM/YYYY)
     * Boundary: European locale
     * Expected: European-formatted date
     */
    @Test
    public void spec_13_formatEU_Locale() {
        // TODO: Locale euLocale = new Locale("de", "DE")
        // TODO: FastDatePrinter euPrinter = 
        //       FastDatePrinter.getInstance("dd.MM.yyyy", euLocale)
        // TODO: Verify DD.MM.YYYY order
    }
    
    // ============== Equivalence Class: Calendar vs Date ##############
    
    /**
     * Spec: Calendar Object Formatting
     * Boundary: Using Calendar instead of Date
     * Expected: Same result as equivalent Date
     */
    @Test
    public void spec_14_formatCalendarEquivalent() {
        // TODO: Date date = new Date()
        // TODO: Calendar cal = Calendar.getInstance()
        // TODO: cal.setTime(date)
        // TODO: String dateResult = printer.format(date)
        // TODO: String calResult = printer.format(cal)
        // TODO: assertEquals(dateResult, calResult)
    }
    
    /**
     * Spec: Milliseconds Timestamp
     * Boundary: Long milliseconds value
     * Expected: Formatted date from timestamp
     */
    @Test
    public void spec_15_formatMillisTimestamp() {
        // TODO: long nowMillis = System.currentTimeMillis()
        // TODO: String result = printer.format(nowMillis)
        // TODO: Verify formatted timestamp
    }
    
    // ============== Test Lifecycle ==============
    
    @Before
    public void setUp() {
        // Initialize printer with default pattern
        printer = FastDatePrinter.getInstance(PATTERN_DATE);
    }
    
    @After
    public void tearDown() {
        printer = null;
    }
}
```

---

## Test Suite 3: FastDateFormat Specification-Based Tests

**Class:** `org.apache.commons.lang3.time.FastDateFormat`  
**Target Methods:** All format variants  
**Current Coverage:** 40-60% (HIGH PRIORITY)  
**Target Coverage:** 75%+

### Implementation File

**Path:** `codebase/src/test/java/org/apache/commons/lang3/time/FastDateFormatSpecTests.java`

```java
package org.apache.commons.lang3.time;

import org.junit.Before;
import org.junit.After;
import org.junit.Test;
import static org.junit.Assert.*;

import java.util.Date;
import java.util.Calendar;
import java.util.Locale;
import java.util.TimeZone;

/**
 * Specification-Based Tests for FastDateFormat
 * 
 * Tests all format() method variants
 * 
 * Coverage Target: 40-60% → 75%+
 * Test Cases: 16
 * Method Variants: 3 (Date, Calendar, long)
 */
public class FastDateFormatSpecTests {
    
    private FastDateFormat formatter;
    private static final String DEFAULT_PATTERN = "yyyy-MM-dd HH:mm:ss";
    
    // ============== Variant 1: Date Object ==============
    
    /**
     * Spec: Format Date Object - Null Input
     * Boundary: date = null
     * Expected: NPE
     */
    @Test(expected = NullPointerException.class)
    public void spec_01_formatDate_null() {
        // TODO: formatter.format((Date) null)
    }
    
    /**
     * Spec: Format Date Object - Current Date
     * Boundary: Today's timestamp
     * Expected: Formatted string matching pattern
     */
    @Test
    public void spec_02_formatDate_current() {
        // TODO: Date now = new Date()
        // TODO: String result = formatter.format(now)
        // TODO: assertNotNull(result)
    }
    
    /**
     * Spec: Format Date Object - Epoch
     * Boundary: 1970-01-01 00:00:00 UTC
     * Expected: Epoch formatted correctly
     */
    @Test
    public void spec_03_formatDate_epoch() {
        // TODO: Date epoch = new Date(0L)
        // TODO: String result = formatter.format(epoch)
        // TODO: assertTrue(result contains "1970")
    }
    
    // ============== Variant 2: Calendar Object ==============
    
    /**
     * Spec: Format Calendar Object - Null Input
     * Boundary: calendar = null
     * Expected: NPE
     */
    @Test(expected = NullPointerException.class)
    public void spec_04_formatCalendar_null() {
        // TODO: formatter.format((Calendar) null)
    }
    
    /**
     * Spec: Format Calendar Object - Current Calendar
     * Boundary: Calendar.getInstance()
     * Expected: Formatted string
     */
    @Test
    public void spec_05_formatCalendar_current() {
        // TODO: Calendar cal = Calendar.getInstance()
        // TODO: String result = formatter.format(cal)
        // TODO: assertNotNull(result)
    }
    
    /**
     * Spec: Format Calendar - Leap Year
     * Boundary: Feb 29 in leap year
     * Expected: Correctly format leap day
     */
    @Test
    public void spec_06_formatCalendar_leapYear() {
        // TODO: Calendar cal = Calendar.getInstance()
        // TODO: cal.set(2020, Calendar.FEBRUARY, 29)
        // TODO: Verify formatting
    }
    
    // ============== Variant 3: Milliseconds (Long) ==============
    
    /**
     * Spec: Format Long Timestamp - Zero
     * Boundary: millis = 0L (epoch)
     * Expected: Formatted epoch
     */
    @Test
    public void spec_07_formatLong_zero() {
        // TODO: String result = formatter.format(0L)
        // TODO: assertTrue(result contains "1970")
    }
    
    /**
     * Spec: Format Long Timestamp - Current
     * Boundary: System.currentTimeMillis()
     * Expected: Current date formatted
     */
    @Test
    public void spec_08_formatLong_current() {
        // TODO: long now = System.currentTimeMillis()
        // TODO: String result = formatter.format(now)
        // TODO: assertNotNull(result)
    }
    
    /**
     * Spec: Format Long Timestamp - Negative
     * Boundary: millis < 0 (before epoch)
     * Expected: Handle pre-1970 dates
     */
    @Test
    public void spec_09_formatLong_negative() {
        // TODO: String result = formatter.format(-86400000L)  // -1 day
        // TODO: Verify handles pre-epoch dates
    }
    
    // ============== Timezone Tests ==============
    
    /**
     * Spec: Timezone Consistency
     * Boundary: Same instant in different timezones
     * Expected: Different local times, same instant
     */
    @Test
    public void spec_10_timezone_consistency() {
        // TODO: FastDateFormat utcFormatter = 
        //       FastDateFormat.getInstance(DEFAULT_PATTERN, TimeZone.getTimeZone("UTC"))
        // TODO: FastDateFormat estFormatter = 
        //       FastDateFormat.getInstance(DEFAULT_PATTERN, TimeZone.getTimeZone("EST"))
        // TODO: long instant = System.currentTimeMillis()
        // TODO: String utcResult = utcFormatter.format(instant)
        // TODO: String estResult = estFormatter.format(instant)
        // TODO: assertNotEquals(utcResult, estResult)  // Different local times
    }
    
    /**
     * Spec: Daylight Saving Time Transition
     * Boundary: DST boundary date
     * Expected: Correct time with DST adjustment
     */
    @Test
    public void spec_11_daylightSavingTime() {
        // TODO: Create formatter with DST-aware timezone
        // TODO: Test at DST transition dates
    }
    
    // ============== Locale Tests ==============
    
    /**
     * Spec: Multiple Locales
     * Boundary: Locale.US vs Locale.FRANCE
     * Expected: Locale-specific formatting
     */
    @Test
    public void spec_12_multipleLocales() {
        // TODO: FastDateFormat usFormatter = 
        //       FastDateFormat.getInstance(DEFAULT_PATTERN, Locale.US)
        // TODO: FastDateFormat frFormatter = 
        //       FastDateFormat.getInstance(DEFAULT_PATTERN, Locale.FRANCE)
        // TODO: Verify locale-specific month/day names if applicable
    }
    
    // ============== Consistency Tests ==============
    
    /**
     * Spec: Date/Calendar Consistency
     * Boundary: Same timestamp in different forms
     * Expected: Same formatted output
     */
    @Test
    public void spec_13_dateCalendarConsistency() {
        // TODO: Date date = new Date()
        // TODO: Calendar cal = Calendar.getInstance()
        // TODO: cal.setTime(date)
        // TODO: String dateResult = formatter.format(date)
        // TODO: String calResult = formatter.format(cal)
        // TODO: assertEquals(dateResult, calResult)
    }
    
    /**
     * Spec: Long/Date Consistency
     * Boundary: Millisecond value vs Date
     * Expected: Same formatted output
     */
    @Test
    public void spec_14_longDateConsistency() {
        // TODO: long millis = System.currentTimeMillis()
        // TODO: Date date = new Date(millis)
        // TODO: String longResult = formatter.format(millis)
        // TODO: String dateResult = formatter.format(date)
        // TODO: assertEquals(longResult, dateResult)
    }
    
    // ============== Thread Safety Tests ==============
    
    /**
     * Spec: Thread-Safe Formatting
     * Boundary: Multiple threads concurrent access
     * Expected: All produce correct output
     * NOTE: FastDateFormat should be thread-safe
     */
    @Test
    public void spec_15_threadSafetyBasic() {
        // TODO: Create multiple threads
        // TODO: All call formatter.format() concurrently
        // TODO: Verify all results are valid
    }
    
    /**
     * Spec: Performance Under Load
     * Boundary: High-frequency formatting
     * Expected: Consistent performance
     */
    @Test
    public void spec_16_performanceUnderLoad() {
        // TODO: Benchmark formatter.format() with 10,000 calls
        // TODO: Verify reasonable performance
    }
    
    // ============== Test Lifecycle ==============
    
    @Before
    public void setUp() {
        formatter = FastDateFormat.getInstance(DEFAULT_PATTERN);
    }
    
    @After
    public void tearDown() {
        formatter = null;
    }
}
```

---

## Test Suite 4: ConstructorUtils Specification-Based Tests

**Class:** `org.apache.commons.lang3.reflect.ConstructorUtils`  
**Target Method:** `invokeConstructor(Class<?> cls, Object... args)`  
**Current Coverage:** 60% (MODERATE)  
**Target Coverage:** 80%+

### Implementation File

**Path:** `codebase/src/test/java/org/apache/commons/lang3/reflect/ConstructorUtilsSpecTests.java`

```java
package org.apache.commons.lang3.reflect;

import org.junit.Before;
import org.junit.After;
import org.junit.Test;
import static org.junit.Assert.*;

import java.util.ArrayList;
import java.util.Date;

/**
 * Specification-Based Tests for ConstructorUtils
 * 
 * Reflection-based constructor invocation testing
 * 
 * Coverage Target: 60% → 80%+
 * Test Cases: 14
 * Focus: Error handling, type matching, edge cases
 */
public class ConstructorUtilsSpecTests {
    
    // ============== Equivalence Class: Standard Classes ==============
    
    /**
     * Spec: String No-Arg Constructor
     * Boundary: String.class with no arguments
     * Expected: Return new String("")
     */
    @Test
    public void spec_01_stringNoArgs() {
        // TODO: Object result = ConstructorUtils.invokeConstructor(String.class)
        // TODO: assertEquals("", result)
        // TODO: assertTrue(result instanceof String)
    }
    
    /**
     * Spec: String with String Constructor
     * Boundary: String.class with String argument
     * Expected: Return new String("Hello")
     */
    @Test
    public void spec_02_stringWithArg() {
        // TODO: Object result = ConstructorUtils.invokeConstructor(String.class, "Hello")
        // TODO: assertEquals("Hello", result)
    }
    
    /**
     * Spec: String with char[] Constructor
     * Boundary: String.class with char array
     * Expected: Convert char array to String
     */
    @Test
    public void spec_03_stringWithCharArray() {
        // TODO: char[] chars = {'H', 'i'}
        // TODO: Object result = ConstructorUtils.invokeConstructor(String.class, chars)
        // TODO: assertEquals("Hi", result)
    }
    
    /**
     * Spec: Integer Constructor
     * Boundary: Integer.class with int
     * Expected: Return Integer object
     */
    @Test
    public void spec_04_integerConstructor() {
        // TODO: Object result = ConstructorUtils.invokeConstructor(Integer.class, 42)
        // TODO: assertTrue(result instanceof Integer)
        // TODO: assertEquals(42, ((Integer)result).intValue())
    }
    
    /**
     * Spec: Date Constructor with Long
     * Boundary: Date.class with milliseconds
     * Expected: Return Date with epoch+millis
     */
    @Test
    public void spec_05_dateWithMillis() {
        // TODO: long millis = 1000L
        // TODO: Object result = ConstructorUtils.invokeConstructor(Date.class, millis)
        // TODO: assertTrue(result instanceof Date)
        // TODO: assertEquals(1000L, ((Date)result).getTime())
    }
    
    /**
     * Spec: ArrayList No-Arg
     * Boundary: ArrayList.class with no args
     * Expected: Return empty ArrayList
     */
    @Test
    public void spec_06_arrayListNoArgs() {
        // TODO: Object result = ConstructorUtils.invokeConstructor(ArrayList.class)
        // TODO: assertTrue(result instanceof ArrayList)
        // TODO: assertTrue(((ArrayList)result).isEmpty())
    }
    
    /**
     * Spec: ArrayList with Capacity
     * Boundary: ArrayList.class with int capacity
     * Expected: Return ArrayList with capacity
     */
    @Test
    public void spec_07_arrayListWithCapacity() {
        // TODO: Object result = ConstructorUtils.invokeConstructor(ArrayList.class, 100)
        // TODO: assertTrue(result instanceof ArrayList)
        // TODO: verify capacity is at least 100
    }
    
    // ============== Equivalence Class: Error Cases ==============
    
    /**
     * Spec: Null Class Parameter
     * Boundary: cls = null
     * Expected: NPE or IllegalArgumentException
     */
    @Test(expected = Exception.class)
    public void spec_08_nullClass() {
        // TODO: ConstructorUtils.invokeConstructor(null)
    }
    
    /**
     * Spec: Abstract Class
     * Boundary: abstract class passed as cls
     * Expected: Error - cannot instantiate abstract class
     */
    @Test(expected = Exception.class)
    public void spec_09_abstractClass() {
        // TODO: Create abstract class and attempt instantiation
        // TODO: Should fail - cannot instantiate abstract
    }
    
    /**
     * Spec: Interface Type
     * Boundary: Interface passed as cls
     * Expected: Error - cannot instantiate interface
     */
    @Test(expected = Exception.class)
    public void spec_10_interfaceType() {
        // TODO: ConstructorUtils.invokeConstructor(java.util.List.class)
        // TODO: Should fail - cannot instantiate interface
    }
    
    /**
     * Spec: Non-Existent Constructor
     * Boundary: No matching constructor for args
     * Expected: Error - constructor not found
     */
    @Test(expected = Exception.class)
    public void spec_11_constructorNotFound() {
        // TODO: ConstructorUtils.invokeConstructor(String.class, 12.34)
        // TODO: String has no double constructor
    }
    
    /**
     * Spec: Primitive Type as Class
     * Boundary: int.class (primitive)
     * Expected: Error - primitive not valid class
     */
    @Test(expected = Exception.class)
    public void spec_12_primitiveType() {
        // TODO: ConstructorUtils.invokeConstructor(int.class)
    }
    
    /**
     * Spec: Private Constructor
     * Boundary: Class with private constructor
     * Expected: May fail or succeed depending on access rules
     * NOTE: Implementation-dependent behavior
     */
    @Test
    public void spec_13_privateConstructor() {
        // TODO: Test class with private constructor
        // TODO: Verify behavior (should likely fail or require accessibility)
    }
    
    /**
     * Spec: Constructor Throwing Exception
     * Boundary: Constructor throws checked exception
     * Expected: Error propagated or wrapped
     */
    @Test(expected = Exception.class)
    public void spec_14_constructorThrowsException() {
        // TODO: Create class whose constructor throws
        // TODO: Invoke and verify exception handling
    }
    
    // ============== Test Lifecycle ==============
    
    @Before
    public void setUp() {
        // Setup test fixtures if needed
    }
    
    @After
    public void tearDown() {
        // Cleanup
    }
}
```

---

## Implementation Checklist

### For Each Test Suite:

- [ ] Create test file in appropriate package
- [ ] Replace TODO comments with actual test code
- [ ] Implement arrange/act/assert patterns
- [ ] Add assertions with meaningful messages
- [ ] Run `mvn test` and verify all tests pass
- [ ] Check code coverage improvements
- [ ] Update testing dashboard

### General Guidelines:

✅ **Do:**
- Use JUnit 4 format (standard @Test, @Before, @After)
- Test one equivalence class per test method
- Include clear test method names (spec_##_description)
- Add JavaDoc comments explaining the specification
- Use meaningful assertions with messages

❌ **Don't:**
- Use JUnit 5 annotations (@ParameterizedTest, @FieldSource)
- Mix multiple equivalence classes in one test
- Leave TODO comments in final code
- Ignore null pointer exceptions without handling
- Assume behavior - verify with assertions

---

## Coverage Validation Workflow

1. **Pre-Implementation Coverage** - Baseline (35-63%)
2. **Implement Test Suite 1** - TypeUtils (spec_01 through spec_12)
3. **Run Coverage Analysis** - `mvn clean test jacoco:report`
4. **Verify Improvement** - Check against baseline
5. **Repeat for Suites 2-4** - FastDatePrinter, FastDateFormat, ConstructorUtils
6. **Final Dashboard Update** - Document total improvements

---

**Status:** Ready for Implementation  
**Expected Timeline:** 1-2 hours per test suite  
**Next Step:** Implement test suite 1, then iterate through suites 2-4

