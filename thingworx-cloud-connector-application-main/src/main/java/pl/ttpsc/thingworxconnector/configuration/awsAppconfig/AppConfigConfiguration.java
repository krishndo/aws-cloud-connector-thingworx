package pl.ttpsc.thingworxconnector.configuration.awsAppconfig;

import com.thingworx.communications.client.ClientConfigurator;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.env.Environment;
import pl.ttpsc.thingworxconnector.configuration.awsAppconfig.AppConfigModule;


/**
 * Thingworx client configuration and instantiation bean
 *
 * @author Maciej Kiciński
 * @version 1.0
 * @since 2021-11-04
 */

@Slf4j
@Configuration
public class AppConfigConfiguration extends ClientConfigurator {

    @Bean
    public AppConfigModule getAppConfigModule(Environment environment) throws Exception {
        log.debug("Processing creation of Aws Appconfig module instance with configuration [{}]", environment);
        return new AppConfigModule(environment);
    }
}
