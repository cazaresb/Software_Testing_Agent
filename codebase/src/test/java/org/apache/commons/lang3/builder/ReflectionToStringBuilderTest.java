package org.apache.commons.lang3.builder;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ReflectionToStringBuilderTest {

    @Test
    void test_toString() {
        // Arrange
        // TODO: initialize parameter 'object' of type 'Object'

        // Act
        var result = ReflectionToStringBuilder.toString(object);

        // Assert
        // TODO: add meaningful assertions
        fail("Not yet implemented");
    }

    @Test
    void test_toString() {
        // Arrange
        // TODO: initialize parameter 'object' of type 'Object'
        // TODO: initialize parameter 'style' of type 'ToStringStyle'

        // Act
        var result = ReflectionToStringBuilder.toString(object, style);

        // Assert
        // TODO: add meaningful assertions
        fail("Not yet implemented");
    }

    @Test
    void test_toString() {
        // Arrange
        // TODO: initialize parameter 'object' of type 'Object'
        // TODO: initialize parameter 'style' of type 'ToStringStyle'
        // TODO: initialize parameter 'outputTransients' of type 'boolean'

        // Act
        var result = ReflectionToStringBuilder.toString(object, style, outputTransients);

        // Assert
        // TODO: add meaningful assertions
        fail("Not yet implemented");
    }

    @Test
    void test_toString() {
        // Arrange
        // TODO: initialize parameter 'object' of type 'Object'
        // TODO: initialize parameter 'style' of type 'ToStringStyle'
        // TODO: initialize parameter 'outputTransients' of type 'boolean'
        // TODO: initialize parameter 'outputStatics' of type 'boolean'

        // Act
        var result = ReflectionToStringBuilder.toString(object, style, outputTransients, outputStatics);

        // Assert
        // TODO: add meaningful assertions
        fail("Not yet implemented");
    }

    @Test
    void test_toString() {
        // Arrange
        // TODO: initialize parameter 'object' of type 'T'
        // TODO: initialize parameter 'style' of type 'ToStringStyle'
        // TODO: initialize parameter 'outputTransients' of type 'boolean'
        // TODO: initialize parameter 'outputStatics' of type 'boolean'
        // TODO: initialize parameter 'reflectUpToClass' of type 'Class'

        // Act
        var result = ReflectionToStringBuilder.toString(object, style, outputTransients, outputStatics, reflectUpToClass);

        // Assert
        // TODO: add meaningful assertions
        fail("Not yet implemented");
    }

    @Test
    void test_toStringExclude() {
        // Arrange
        // TODO: initialize parameter 'object' of type 'Object'
        // TODO: initialize parameter 'excludeFieldNames' of type 'Collection'

        // Act
        var result = ReflectionToStringBuilder.toStringExclude(object, excludeFieldNames);

        // Assert
        // TODO: add meaningful assertions
        fail("Not yet implemented");
    }

    @Test
    void test_toStringExclude() {
        // Arrange
        // TODO: initialize parameter 'object' of type 'Object'
        // TODO: initialize parameter 'excludeFieldNames' of type 'String'

        // Act
        var result = ReflectionToStringBuilder.toStringExclude(object, excludeFieldNames);

        // Assert
        // TODO: add meaningful assertions
        fail("Not yet implemented");
    }

    @Test
    void test_getExcludeFieldNames() {
        // Arrange
        ReflectionToStringBuilder obj = new ReflectionToStringBuilder();

        // Act
        var result = obj.getExcludeFieldNames();

        // Assert
        // TODO: add meaningful assertions
        fail("Not yet implemented");
    }

    @Test
    void test_getUpToClass() {
        // Arrange
        ReflectionToStringBuilder obj = new ReflectionToStringBuilder();

        // Act
        var result = obj.getUpToClass();

        // Assert
        // TODO: add meaningful assertions
        fail("Not yet implemented");
    }

    @Test
    void test_isAppendStatics() {
        // Arrange
        ReflectionToStringBuilder obj = new ReflectionToStringBuilder();

        // Act
        var result = obj.isAppendStatics();

        // Assert
        // TODO: add meaningful assertions
        fail("Not yet implemented");
    }

    @Test
    void test_isAppendTransients() {
        // Arrange
        ReflectionToStringBuilder obj = new ReflectionToStringBuilder();

        // Act
        var result = obj.isAppendTransients();

        // Assert
        // TODO: add meaningful assertions
        fail("Not yet implemented");
    }

    @Test
    void test_reflectionAppendArray() {
        // Arrange
        ReflectionToStringBuilder obj = new ReflectionToStringBuilder();
        // TODO: initialize parameter 'array' of type 'Object'

        // Act
        var result = obj.reflectionAppendArray(array);

        // Assert
        // TODO: add meaningful assertions
        fail("Not yet implemented");
    }

    @Test
    void test_setAppendStatics() {
        // Arrange
        ReflectionToStringBuilder obj = new ReflectionToStringBuilder();
        // TODO: initialize parameter 'appendStatics' of type 'boolean'

        // Act
        obj.setAppendStatics(appendStatics);

        // Assert
        // TODO: add meaningful assertions
        fail("Not yet implemented");
    }

    @Test
    void test_setAppendTransients() {
        // Arrange
        ReflectionToStringBuilder obj = new ReflectionToStringBuilder();
        // TODO: initialize parameter 'appendTransients' of type 'boolean'

        // Act
        obj.setAppendTransients(appendTransients);

        // Assert
        // TODO: add meaningful assertions
        fail("Not yet implemented");
    }

    @Test
    void test_setExcludeFieldNames() {
        // Arrange
        ReflectionToStringBuilder obj = new ReflectionToStringBuilder();
        // TODO: initialize parameter 'excludeFieldNamesParam' of type 'String'

        // Act
        var result = obj.setExcludeFieldNames(excludeFieldNamesParam);

        // Assert
        // TODO: add meaningful assertions
        fail("Not yet implemented");
    }

    @Test
    void test_setUpToClass() {
        // Arrange
        ReflectionToStringBuilder obj = new ReflectionToStringBuilder();
        // TODO: initialize parameter 'clazz' of type 'Class'

        // Act
        obj.setUpToClass(clazz);

        // Assert
        // TODO: add meaningful assertions
        fail("Not yet implemented");
    }

    @Test
    void test_toString() {
        // Arrange
        ReflectionToStringBuilder obj = new ReflectionToStringBuilder();

        // Act
        var result = obj.toString();

        // Assert
        // TODO: add meaningful assertions
        fail("Not yet implemented");
    }

    @Test
    void test_ReflectionToStringBuilderConstructor() {
        // Arrange
        // TODO: initialize parameter 'object' of type 'Object'

        // Act
        ReflectionToStringBuilder(object);

        // Assert
        // TODO: add meaningful assertions
        fail("Not yet implemented");
    }

    @Test
    void test_ReflectionToStringBuilderConstructor() {
        // Arrange
        // TODO: initialize parameter 'object' of type 'Object'
        // TODO: initialize parameter 'style' of type 'ToStringStyle'

        // Act
        ReflectionToStringBuilder(object, style);

        // Assert
        // TODO: add meaningful assertions
        fail("Not yet implemented");
    }

    @Test
    void test_ReflectionToStringBuilderConstructor() {
        // Arrange
        // TODO: initialize parameter 'object' of type 'Object'
        // TODO: initialize parameter 'style' of type 'ToStringStyle'
        // TODO: initialize parameter 'buffer' of type 'StringBuffer'

        // Act
        ReflectionToStringBuilder(object, style, buffer);

        // Assert
        // TODO: add meaningful assertions
        fail("Not yet implemented");
    }

    @Test
    void test_ReflectionToStringBuilderConstructor() {
        // Arrange
        // TODO: initialize parameter 'object' of type 'T'
        // TODO: initialize parameter 'style' of type 'ToStringStyle'
        // TODO: initialize parameter 'buffer' of type 'StringBuffer'
        // TODO: initialize parameter 'reflectUpToClass' of type 'Class'
        // TODO: initialize parameter 'outputTransients' of type 'boolean'
        // TODO: initialize parameter 'outputStatics' of type 'boolean'

        // Act
        ReflectionToStringBuilder(object, style, buffer, reflectUpToClass, outputTransients, outputStatics);

        // Assert
        // TODO: add meaningful assertions
        fail("Not yet implemented");
    }

}